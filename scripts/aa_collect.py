# -*- coding: utf-8 -*-
"""
AA 模型数据采集脚本 — Artificial Analysis 数据更新

用途: 抓取 artificialanalysis.ai/models 的 JSON-LD 结构化数据,
      合并成按模型聚合的记录, 写入采集/采集表/aa_models.md(机器可读 JSON)。
      可选: 重新生成 docs/词条/04-LLM工程/模型数据总览.md 的表格。

用法:
  python scripts/aa_collect.py                 # 只更新采集表
  python scripts/aa_collect.py --with-entry    # 更新采集表 + 重写词条表格

依赖: 仅标准库(urllib)。需代理时可设环境变量 AA_PROXY(如 http://127.0.0.1:7892)。

规则: 数据状态置为 proposed, 正式引用前需人工审核(见 _readme.md 采集表规范)。
"""
import json
import os
import re
import sys
import urllib.request
from datetime import date

URL = "https://artificialanalysis.ai/models"
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
COLLECT_PATH = os.path.join(PROJ, "采集", "采集表", "aa_models.md")
ENTRY_PATH = os.path.join(PROJ, "docs", "词条", "04-LLM工程", "模型数据总览.md")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def fetch(url: str) -> str:
    """用 curl 抓取(urllib 走代理有 SSL EOF 问题, curl 已验证稳定)"""
    import subprocess
    import time
    cmd = ["curl", "-s", "-L", url, "-A", UA, "--max-time", "150"]
    proxy = os.environ.get("AA_PROXY")
    if proxy:
        cmd += ["-x", proxy]
    last_err = ""
    for attempt in range(3):  # 手册 §9.2: 最多 3 次, 指数退避
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode == 0 and r.stdout:
            return r.stdout
        last_err = f"attempt {attempt+1}: rc={r.returncode} {r.stderr[:150]}"
        time.sleep(2 ** attempt)
    raise RuntimeError(f"curl failed after 3 attempts: {last_err}")


def parse_datasets(html: str):
    """提取 HTML 中所有 application/ld+json 的 Dataset 块"""
    datasets = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            j = json.loads(m.group(1))
        except Exception:
            continue
        if j.get("@type") == "Dataset":
            datasets.append(j)
    return datasets


def merge_models(datasets):
    merged = {}
    for d in datasets:
        for rec in d.get("data", []):
            label = rec["label"]
            m = merged.setdefault(label, {"label": label, "url": rec.get("detailsUrl", "")})
            for k, v in rec.items():
                if k in ("label", "detailsUrl"):
                    continue
                if isinstance(v, list):
                    for pv in v:
                        if isinstance(pv, dict) and pv.get("@type") == "PropertyValue":
                            m[pv["name"]] = pv["value"]
                else:
                    m[k] = v
    return merged


def build_records(merged, today):
    records = []
    for label in sorted(merged):
        m = merged[label]
        url = m.get("url", "")
        if url and not url.startswith("http"):
            url = "https://artificialanalysis.ai" + url
        records.append({
            "id": "SRC-AA-%04d" % (len(records) + 1),
            "title": label,
            "url": url,
            "type": "benchmark",
            "language": "en",
            "publisher": "Artificial Analysis",
            "domains": ["LLM/评测/模型数据"],
            "target_terms": ["模型数据总览", "模型评测"],
            "angle": "独立第三方 AI 模型横评:智能指数/价格/速度/上下文/开放度",
            "quality": "A",
            "status": "proposed",
            "tier": "A",
            "collected": today,
            "data": {k: v for k, v in m.items() if k not in ("label", "url")},
        })
    return records


def write_collect(records, today):
    lines = ["# AA 模型数据采集表", ""]
    lines.append(f"> 来源: {URL} | 采集: {today} | 状态: proposed(未审核)")
    lines.append("> 规则: 本文件是 JSON 数组,机器可读;正式引用前需人工审核。由 scripts/aa_collect.py 维护。")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(records, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    with open(COLLECT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] 采集表更新: {COLLECT_PATH} ({len(records)} 模型)")


def rnd(x, n=2):
    try:
        v = float(x)
        return round(v, n)
    except Exception:
        return "—"


def fmt_price(x):
    v = rnd(x, 2)
    return "—" if v == "—" else f"${v}"


def fmt_ctx(x):
    if not x:
        return "—"
    v = int(x)
    if v >= 1_000_000:
        s = v / 1_000_000
        return f"{s:g}M" if s == int(s) else f"{s:.1f}M"
    return f"{v / 1000:g}K"


def gen_tables(merged):
    """生成词条里的两张表(智能排序 + 速度排序)"""
    rows = []
    for label in sorted(merged):
        m = merged[label]
        rows.append({
            "label": label,
            "ii": rnd(m.get("intelligenceIndex")),
            "sp": rnd(m.get("outputSpeed"), 1),
            "inp": fmt_price(m.get("inputPrice")),
            "out": fmt_price(m.get("outputPrice")),
            "ctx": fmt_ctx(m.get("contextWindowTokens")),
            "op": rnd(m.get("opennessIndex")),
        })

    header = "| 模型 | 智能指数 | 输出速度 (tok/s) | 输入价 $/M | 输出价 $/M | 上下文 | 开放度 |"
    sep = "|------|---------|-----------------|-----------|-----------|--------|--------|"

    def render(rows):
        out = [header, sep]
        for r in rows:
            out.append(f"| {r['label']} | {r['ii']} | {r['sp']} | {r['inp']} | {r['out']} | {r['ctx']} | {r['op']} |")
        return "\n".join(out)

    by_ii = sorted(rows, key=lambda r: (r["ii"] == "—", -(r["ii"] if r["ii"] != "—" else 0)))
    by_sp = sorted(rows, key=lambda r: (r["sp"] == "—", -(r["sp"] if r["sp"] != "—" else 0)))[:10]
    sp_header = "| 模型 | 输出速度 (tok/s) | 智能指数 | 输入价 $/M | 输出价 $/M |"
    sp_sep = "|------|-----------------|---------|-----------|-----------|"
    sp_lines = [sp_header, sp_sep]
    for r in by_sp:
        sp_lines.append(f"| {r['label']} | {r['sp']} | {r['ii']} | {r['inp']} | {r['out']} |")
    return render(by_ii), "\n".join(sp_lines)


def update_entry(merged, today):
    """用表格内容更新词条(只替换两个表格区块,其余正文不动)"""
    if not os.path.exists(ENTRY_PATH):
        print(f"[SKIP] 词条不存在: {ENTRY_PATH}")
        return
    ii_table, sp_table = gen_tables(merged)
    with open(ENTRY_PATH, encoding="utf-8") as f:
        content = f.read()

    def replace_block(content, start_marker, end_marker, new_block):
        i = content.find(start_marker)
        j = content.find(end_marker, i)
        if i < 0 or j < 0:
            return content, False
        return content[:i] + start_marker + "\n" + new_block + content[j:], True

    content, ok1 = replace_block(content, "按智能指数排序：\n", "\n\n按输出速度排序", ii_table)
    content, ok2 = replace_block(content, "按输出速度排序（速度前十）:\n", "\n\n> 完整原始数据", sp_table)
    # 更新采集日期
    content = re.sub(r"（\d{4}-\d{2}-\d{2} 抓取）", f"（{today} 抓取）", content)
    content = re.sub(r"### 当前数据（.*?）", f"### 当前数据（{today} 抓取）", content)
    with open(ENTRY_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] 词条表格更新: {ENTRY_PATH} (block1={ok1}, block2={ok2})")


def main():
    today = date.today().isoformat()
    print(f"抓取 {URL} ...")
    html = fetch(URL)
    datasets = parse_datasets(html)
    if not datasets:
        print("[FAIL] 未解析到 Dataset 数据, 页面结构可能变更")
        sys.exit(1)
    merged = merge_models(datasets)
    print(f"解析到 {len(datasets)} 个数据集, {len(merged)} 个模型")
    records = build_records(merged, today)
    write_collect(records, today)
    if "--with-entry" in sys.argv:
        update_entry(merged, today)


if __name__ == "__main__":
    main()
