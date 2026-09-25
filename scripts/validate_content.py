#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
词条 Schema 校验器 —— DESIGN-SPEC 第四节《Schema 校验规则》的可执行版本。

为什么要它：DESIGN-SPEC 第 101 行写了「字段缺失、无来源、格式不对 → 自动打回（CI 校验）」，
第 128 行规划了 .github/workflows/validate.yml —— 这两处此前都只存在于文档里。
结果是 5 条关系边指向了不存在的词条、1 组重名（DeepSeek）长期无人发现。

规则来源：docs/项目文档/DESIGN-SPEC.md
  §4 词条 Schema / Schema 校验规则（强制）
  §5 成熟度分级
  §7 质量门流水线第 2 道

关键设计：**区分 draft 与 published**
  骨架词条（draft）允许无来源——它本来就还没到收录标准，只是占位。
  published 才受「无源不收录」约束。这样 CI 从第一天起就能全绿，而不是靠豁免清单糊住。

用法：
  python3 scripts/validate_content.py              # 错误 → 退出码 1；警告仅提示
  python3 scripts/validate_content.py --strict     # 警告也算失败（内容稳定后可在 CI 打开）
  python3 scripts/validate_content.py --json       # 机器可读输出
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

try:
    import yaml
except ImportError:  # pragma: no cover
    print("缺少 pyyaml：pip install pyyaml", file=sys.stderr)
    raise SystemExit(2)

# ---------------------------------------------------------------- 常量

TERM_DIR = os.path.join("docs", "词条")

# 必须"有值"的字段。sources 单列：键必须存在，但 draft 阶段允许是空列表，
# 见下面第 5 条规则（published 才受「无源不收录」约束）。
REQUIRED_FIELDS = ["term", "full_name", "category", "maturity", "status"]
REQUIRED_KEYS = ["sources"]

MATURITY_OK = {"stable", "hot"}
STATUS_OK = {"draft", "review", "published"}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_RE = re.compile(r"^https?://\S+$")

# 正文里必须出现的章节（DESIGN-SPEC §4 词条模板）
REQUIRED_SECTION = "## 定义"

HOT_MARK = "[热词]"
SKELETON_MARK = "[骨架]"

# 关系类型合法值（未登记的值只警告，不拦——允许它长出来）
# 前 7 个是当前语料里真实在用的（语料统计：applies_to 86 / part_of 41 / contrast 15 /
# evolved_from 5 / similar_to 4 / prerequisite 3 / peer 3），其余为预留。
# 注意 `prerequisite` 与 `peer` —— 前者是「先修链」的原料，后者是水平对照关系。
KNOWN_REL_TYPES = {
    "applies_to", "part_of", "contrast", "evolved_from", "similar_to", "prerequisite", "peer",
    "related", "instance_of", "uses", "used_by", "depends_on",
}


# ---------------------------------------------------------------- 数据结构

class Issue:
    __slots__ = ("level", "code", "path", "msg")

    def __init__(self, level: str, code: str, path: str, msg: str):
        self.level, self.code, self.path, self.msg = level, code, path, msg

    def __str__(self) -> str:
        tag = "ERROR" if self.level == "error" else "WARN "
        return f"  [{tag}] {self.path}  {self.msg}   ({self.code})"


def load_terms(root: str):
    """读出全部词条的 frontmatter 与正文。保持宽松——校验器自己负责报告残缺。"""
    terms = []
    for cur, _, files in os.walk(os.path.join(root, TERM_DIR)):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            full = os.path.join(cur, fn)
            rel = os.path.relpath(full, os.path.join(root, TERM_DIR)).replace("\\", "/")
            raw = open(full, encoding="utf-8").read()

            meta, body, fm_error = {}, "", None
            if raw.startswith("---"):
                parts = raw.split("---", 2)
                if len(parts) >= 3:
                    try:
                        meta = yaml.safe_load(parts[1]) or {}
                    except yaml.YAMLError as e:
                        fm_error = f"frontmatter 解析失败：{str(e)[:80]}"
                    body = parts[2]
                else:
                    fm_error = "frontmatter 未闭合（缺少结尾的 ---）"
            else:
                fm_error = "文件未以 frontmatter 开头"

            if not isinstance(meta, dict):
                fm_error = fm_error or "frontmatter 不是键值结构"
                meta = {}

            seg = rel.split("/")
            terms.append({
                "path": rel,
                "file": fn,
                "meta": meta,
                "body": body,
                "fm_error": fm_error,
                "group": seg[0] if seg else "",
                "subgroup": seg[1] if len(seg) > 2 else "",
            })
    return terms


# ---------------------------------------------------------------- 校验

def validate(terms):
    issues: list[Issue] = []

    # ---- 0. frontmatter 本身可解析
    for t in terms:
        if t["fm_error"]:
            issues.append(Issue("error", "FM-PARSE", t["path"], t["fm_error"]))

    terms = [t for t in terms if not t["fm_error"]]

    # ---- 索引：term / alias 的解析表
    by_term = defaultdict(list)
    for t in terms:
        if t["meta"].get("term"):
            by_term[t["meta"]["term"]].append(t)

    resolvable = set(by_term)
    alias_owner = {}
    for t in terms:
        for a in t["meta"].get("aliases") or []:
            a = str(a).strip()
            if a:
                alias_owner.setdefault(a, t["meta"].get("term"))
                resolvable.add(a)

    # ---- 1. 必填字段
    for t in terms:
        m = t["meta"]
        for f in REQUIRED_FIELDS:
            if f not in m or m[f] in (None, "", [], {}):
                issues.append(Issue("error", "REQ-MISSING", t["path"], f"缺少必填字段 `{f}`"))
        for f in REQUIRED_KEYS:
            if f not in m:
                issues.append(Issue("error", "REQ-KEY", t["path"], f"缺少字段 `{f}`（可以为空列表，但必须显式声明）"))

    # ---- 2. term 唯一（图谱完整性：边靠它定位目标）
    for term, group in sorted(by_term.items()):
        if len(group) > 1:
            paths = ", ".join(g["path"] for g in group)
            for g in group:
                issues.append(Issue("error", "TERM-DUP", g["path"], f"`term: {term}` 重复出现于：{paths}"))

    # ---- 3. 枚举值
    for t in terms:
        m = t["meta"]
        if m.get("maturity") and m["maturity"] not in MATURITY_OK:
            issues.append(Issue("error", "ENUM-MATURITY", t["path"],
                                f"maturity=`{m['maturity']}` 不在 {sorted(MATURITY_OK)}"))
        if m.get("status") and m["status"] not in STATUS_OK:
            issues.append(Issue("error", "ENUM-STATUS", t["path"],
                                f"status=`{m['status']}` 不在 {sorted(STATUS_OK)}"))

    # ---- 4. 日期与修订号
    for t in terms:
        m = t["meta"]
        for f in ("created", "updated"):
            v = m.get(f)
            if v is None:
                continue
            if isinstance(v, str) and not DATE_RE.match(v.strip()):
                issues.append(Issue("error", "DATE-FMT", t["path"],
                                    f"{f}=`{v}` 不是 YYYY-MM-DD"))
        r = m.get("revisions")
        if r is not None and (not isinstance(r, int) or r < 1):
            issues.append(Issue("error", "REVISION", t["path"], f"revisions=`{r}` 应为 ≥1 的整数"))

    # ---- 5. sources：published 强制有源（DESIGN-SPEC「无源不收录」）
    for t in terms:
        m = t["meta"]
        srcs = [str(s) for s in (m.get("sources") or [])]
        good = [s for s in srcs if URL_RE.match(s.strip())]
        bad = [s for s in srcs if s.strip() and not URL_RE.match(s.strip())]
        is_published = m.get("status") == "published"

        if bad:
            issues.append(Issue("error", "SRC-FMT", t["path"],
                                f"来源不是有效 URL：{bad}"))
        if is_published and not good:
            issues.append(Issue("error", "SRC-EMPTY-PUB", t["path"],
                                "status=published 但没有任何有效来源（无源不收录）"))
        elif not is_published and not good:
            issues.append(Issue("warn", "SRC-EMPTY-DRAFT", t["path"],
                                f"无来源（status={m.get('status')}，draft 阶段可接受）"))

    # ---- 6. relations：目标必须可解析（图谱的边不能悬空）
    for t in terms:
        for r in t["meta"].get("relations") or []:
            if isinstance(r, dict):
                target, rtype = r.get("target"), r.get("type")
                note = r.get("note")
            else:
                target, rtype, note = r, None, None

            target = str(target).strip() if target else ""
            if not target:
                issues.append(Issue("error", "REL-NOTARGET", t["path"], "有一条关系缺少 target"))
                continue
            if target not in resolvable:
                issues.append(Issue("error", "REL-DANGLING", t["path"],
                                    f"关系目标 `{target}` 找不到对应词条，也不匹配任何别名 → 断边"))
            if target == t["meta"].get("term"):
                issues.append(Issue("warn", "REL-SELF", t["path"],
                                    f"关系 `{target}` 指向自己"))
            if rtype and rtype not in KNOWN_REL_TYPES:
                issues.append(Issue("warn", "REL-TYPE-NEW", t["path"],
                                    f"关系类型 `{rtype}` 未登记"))

    # ---- 7. 正文结构
    for t in terms:
        body = t["body"]
        if REQUIRED_SECTION not in body:
            issues.append(Issue("error", "BODY-SECTION", t["path"], f"正文缺少 `{REQUIRED_SECTION}` 章节"))
        if len(body.strip()) < 40:
            issues.append(Issue("error", "BODY-SHORT", t["path"], "正文过短（<40 字符）"))

    # ---- 8. 成熟度标注（DESIGN-SPEC §5）
    for t in terms:
        if t["meta"].get("maturity") == "hot" and HOT_MARK not in t["body"][:400]:
            issues.append(Issue("warn", "HOT-UNMARKED", t["path"],
                                f"maturity=hot 但正文未标 `{HOT_MARK}` 提示"))

    # ---- 9. 可选字段的完整性（提醒，不拦）
    for t in terms:
        m = t["meta"]
        if not m.get("aliases"):
            issues.append(Issue("warn", "ALIAS-EMPTY", t["path"], "没有别名，检索命中率会低"))
        if not m.get("relations"):
            issues.append(Issue("warn", "REL-EMPTY", t["path"], "没有任何关系，在图谱里是孤岛"))
        if t["file"][:-3] != m.get("term"):
            issues.append(Issue("warn", "FILENAME", t["path"],
                                f"文件名 `{t['file'][:-3]}` 与 term `{m.get('term')}` 不一致"))

    return issues, terms


# ---------------------------------------------------------------- 报告

def report(issues, terms, as_json: bool) -> int:
    errors = [i for i in issues if i.level == "error"]
    warns = [i for i in issues if i.level == "warn"]

    if as_json:
        print(json.dumps({
            "terms": len(terms),
            "errors": len(errors),
            "warnings": len(warns),
            "issues": [{"level": i.level, "code": i.code, "path": i.path, "msg": i.msg} for i in issues],
        }, ensure_ascii=False, indent=2))
        return 1 if errors else 0

    by_code = Counter(i.code for i in issues)
    cats = defaultdict(list)
    for t in terms:
        cats[t["meta"].get("status") or "(无 status)"].append(t)

    print()
    print("词条 Schema 校验")
    print("=" * 62)
    print(f"  词条总数 {len(terms)}    " + "   ".join(f"{k} {len(v)}" for k, v in sorted(cats.items())))
    print()

    if not issues:
        print("  ✓ 全部通过，没有发现任何问题。")
        print()
        return 0

    # 错误明细
    if errors:
        print(f"✗ 错误 {len(errors)} 条（会阻断发布）")
        print("-" * 62)
        grouped = defaultdict(list)
        for e in errors:
            grouped[e.code].append(e)
        for code, items in sorted(grouped.items()):
            print(f"\n  ▸ {code}（{len(items)}）")
            for e in items[:8]:
                print(f"      {e.path}")
                print(f"        {e.msg}")
            if len(items) > 8:
                print(f"      … 另有 {len(items) - 8} 条同类")
        print()

    # 警告汇总（不逐条铺开，只给计数，避免淹没重点）
    if warns:
        print(f"! 警告 {len(warns)} 条（不阻断）")
        print("-" * 62)
        for code, n in sorted(Counter(w.code for w in warns).items(), key=lambda x: -x[1]):
            sample = next(w for w in warns if w.code == code)
            print(f"  {n:4d}  {code:18s} {sample.msg}")
        print()

    print("=" * 62)
    if errors:
        print(f"结果：不通过（{len(errors)} 错误 / {len(warns)} 警告）")
    else:
        print(f"结果：通过（{len(warns)} 警告，不阻断）")
    print()
    return 1 if errors else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="词条 Schema 校验（DESIGN-SPEC §4）")
    ap.add_argument("--root", default=".", help="仓库根目录")
    ap.add_argument("--strict", action="store_true", help="警告也视为失败")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    terms = load_terms(args.root)
    if not terms:
        print(f"未找到任何词条：{os.path.join(args.root, TERM_DIR)}", file=sys.stderr)
        return 2

    issues, terms = validate(terms)
    code = report(issues, terms, args.json)

    if args.strict and code == 0:
        warns = [i for i in issues if i.level == "warn"]
        if warns and not args.json:
            print(f"--strict 已开启：{len(warns)} 条警告视为失败\n")
        code = 1 if warns else 0

    return code


if __name__ == "__main__":
    raise SystemExit(main())
