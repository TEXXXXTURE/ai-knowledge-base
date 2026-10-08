# -*- coding: utf-8 -*-
"""
MOKE AIGC 文章采集脚本 — 文章推送功能的内容源

用途: 抓取 mokeaigc.com 的每日日报与文章详情, 落采集表 JSON,
      作为 wiki「文章与引用」栏目的内容填充。

数据源(均为公开端点, 无需登录):
  - 日报结构:  GET /api/daily/latest            → issue + sections[].items[].articleId
  - 文章详情:  GET /api/entries/{id}?publicPage=daily → payload.entry

用法:
  python scripts/moke_collect.py                 # 抓最新日报 + 全部文章
  python scripts/moke_collect.py --max-articles 10   # 只抓前 N 篇(测试用)
  python scripts/moke_collect.py --cache-dir C:/tmp  # 指定缓存目录

依赖: 标准库 + curl(走代理时设 MOKE_PROXY, 如 http://127.0.0.1:7892)
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime

BASE = "https://www.mokeaigc.com"
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
OUT_PATH = os.path.join(PROJ, "采集", "采集表", "moke_articles.md")
CACHE_DIR = os.environ.get("MOKE_CACHE", r"C:\tmp")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def fetch(url: str, timeout: int = 60) -> str:
    """curl 抓取(urllib 走代理有 SSL EOF 问题, 统一用 curl)"""
    cmd = ["curl", "-s", "-L", url, "-A", UA, "-H", "accept: application/json", "--max-time", str(timeout)]
    proxy = os.environ.get("MOKE_PROXY")
    if proxy:
        cmd += ["-x", proxy]
    last_err = ""
    for attempt in range(3):
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode == 0 and r.stdout:
            return r.stdout
        last_err = f"attempt {attempt+1}: rc={r.returncode} {r.stderr[:120]}"
        time.sleep(2 ** attempt)
    raise RuntimeError(f"curl failed: {last_err}")


def get_json(url: str):
    text = fetch(url)
    try:
        return json.loads(text)
    except Exception:
        # 有些端点返回 HTML 错误页
        return None


def get_daily_issue():
    """抓最新日报结构"""
    data = get_json(f"{BASE}/api/daily/latest")
    if not data or "issue" not in data:
        raise RuntimeError("日报结构获取失败(api/daily/latest)")
    return data["issue"]


def get_entry(entry_id: str):
    """抓单篇文章详情"""
    url = f"{BASE}/api/entries/{entry_id}?publicPage=daily"
    # 走缓存
    cache = os.path.join(CACHE_DIR, f"moke-entry-{entry_id}.json")
    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as f:
            return json.load(f).get("entry")
    data = get_json(url)
    if not data:
        return None
    entry = data.get("entry")
    if entry:
        with open(cache, "w", encoding="utf-8") as f:
            json.dump({"entry": entry}, f, ensure_ascii=False)
    return entry


def main():
    max_articles = None
    args = sys.argv[1:]
    if "--max-articles" in args:
        i = args.index("--max-articles")
        max_articles = int(args[i + 1])

    print("抓取日报结构 ...")
    issue = get_daily_issue()
    issue_id = issue.get("id", "")
    issue_date = issue.get("issue_date", "")
    volume = issue.get("volume_no", "")
    title = issue.get("title", "")
    print(f"  日报: {title} ({issue_date}) | {issue.get('story_count')} 篇 | {issue.get('reading_minutes')} 分钟")

    # 收集所有 articleId
    ids = []
    sections = []
    for sec in issue.get("sections", []):
        items = sec.get("items", [])
        sec_info = {"section_key": sec.get("section_key"), "title_zh": sec.get("title_zh"),
                    "position": sec.get("position"), "count": len(items)}
        sections.append(sec_info)
        for item in items:
            ids.append(item.get("articleId"))

    ids = list(dict.fromkeys(ids))  # 去重保序
    if max_articles:
        ids = ids[:max_articles]
    print(f"  共 {len(ids)} 篇文章待抓取")

    # 抓文章
    entries = []
    fails = []
    for i, eid in enumerate(ids, 1):
        try:
            e = get_entry(eid)
            if e:
                entries.append(e)
                print(f"  [{i}/{len(ids)}] ✓ {e.get('titleZh') or e.get('title', '')[:40]}")
            else:
                fails.append(eid)
                print(f"  [{i}/{len(ids)}] ✗ 空响应 {eid[:8]}")
        except Exception as ex:
            fails.append(eid)
            print(f"  [{i}/{len(ids)}] ✗ {str(ex)[:60]}")
        time.sleep(0.3)  # 礼貌限速

    print(f"\n成功 {len(entries)} / {len(ids)}, 失败 {len(fails)}")

    # 落采集表
    records = []
    for e in entries:
        url = e.get("url", "")
        published = e.get("publishedAt")
        pub_date = datetime.fromtimestamp(published / 1000).strftime("%Y-%m-%d") if published else ""
        records.append({
            "id": f"MOKE-{e.get('id', '')[:8]}",
            "title": e.get("titleZh") or e.get("title", ""),
            "title_original": e.get("titleOriginal") or e.get("title", ""),
            "url": url,
            "type": "article",
            "language": "zh",
            "publisher": e.get("feedTitle") or e.get("sourceName") or "MOKE",
            "platform": e.get("platformName", ""),
            "author": e.get("author", ""),
            "author_url": e.get("authorUrl", ""),
            "domains": ["AI/资讯"],
            "target_terms": e.get("tags", []),
            "angle": e.get("description", ""),
            "quality": "B",
            "status": "proposed",
            "tier": "B",
            "collected": datetime.now().strftime("%Y-%m-%d"),
            "published": pub_date,
            "issue": volume,
            "category": e.get("category", ""),
            "content_format": e.get("contentFormat", ""),
            "score": e.get("score", 0),
            "summary_zh": e.get("summaryZh", ""),
            "summary_en": e.get("summaryEn", ""),
            "reason": e.get("reason", ""),
            "content": e.get("content", ""),
        })

    lines = ["# MOKE 文章采集表", ""]
    lines.append(f"> 来源: {BASE} | 采集: {datetime.now().strftime('%Y-%m-%d')} | 状态: proposed(未审核)")
    lines.append(f"> 日报: {title} ({issue_date}) | 板块: {json.dumps(sections, ensure_ascii=False)}")
    lines.append("> 规则: 本文件是 JSON 数组,机器可读;正式引用前需人工审核。由 scripts/moke_collect.py 维护。")
    lines.append("> 版权: 仅收录聚合摘要/判断线索/阅读索引, 正文全文按 MOKE 声明归各来源权利人所有。")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(records, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n[OK] 采集表更新: {OUT_PATH} ({len(records)} 篇文章)")
    if fails:
        print(f"[WARN] {len(fails)} 篇失败: {[f[:8] for f in fails]}")


if __name__ == "__main__":
    main()
