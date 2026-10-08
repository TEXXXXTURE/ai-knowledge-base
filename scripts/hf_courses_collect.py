"""HF Learn 全课程采集 v3 — 章节遍历策略
首页只暴露少量链接，完整单元列表在章节导航里。
策略：解析首页拿到章节数/单元数范围，遍历抓取 .md。
"""
import urllib.request, re, time, os, socket

socket.setdefaulttimeout(25)
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
BASE = "https://huggingface.co"

def fetch(url, retry=3):
    for i in range(retry):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode('utf-8', errors='replace')
        except Exception as e:
            if i == retry - 1:
                return None
            time.sleep(2 * (i + 1))
    return None

def get_unit_paths(course):
    """从首页提取单元路径（含 md 链接 + 章节导航）"""
    html = fetch(f"{BASE}/learn/{course}")
    if not html:
        return []
    # 方式1：显式 .md 链接
    units = re.findall(rf'href="/learn/{course}/([^"/]+\.md)"', html)
    # 方式2：章节导航链接（chapterX/Y 或 unitX/Y 或 unitX/name）
    units += re.findall(rf'href="/learn/{course}/((?:chapter|unit)\d+/[^"?]+)"', html)
    # 去重保序
    seen, out = set(), []
    for u in units:
        u = u.replace('.md', '')
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out

COURSES = ["llm-course", "context-course", "smol-course", "agents-course",
           "deep-rl-course", "audio-course", "cookbook", "ml-games-course",
           "computer-vision-course", "ml-for-3d-course", "robotics-course"]

OUT = r"D:\AIGC术语库\采集\采集\hf-courses"
os.makedirs(OUT, exist_ok=True)

summary = []
for course in COURSES:
    paths = get_unit_paths(course)
    if not paths:
        print(f"⚠️ {course}: 未找到单元")
        continue
    cdir = os.path.join(OUT, course)
    os.makedirs(cdir, exist_ok=True)
    got = 0
    for unit in paths:
        url = f"{BASE}/learn/{course}/{unit}.md"
        md = fetch(url)
        if md and len(md) > 100 and "404" not in md[:100]:
            fn = unit.replace("/", "-") + ".md"
            with open(os.path.join(cdir, fn), "w", encoding="utf-8") as f:
                f.write(f"# 来源: {url}\n\n" + md)
            got += 1
        time.sleep(1.2)
    summary.append((course, len(paths), got))
    print(f"✅ {course}: {got}/{len(paths)} 单元")

print("\n===== 汇总 =====")
for c, total, got in summary:
    print(f"  {c}: {got}/{total}")
