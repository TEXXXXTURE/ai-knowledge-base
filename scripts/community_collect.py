"""社区采集脚本 — AIGC 术语知识库
从 GitHub Issues/Discussions、Reddit、HuggingFace 讨论区抓取社区一线讨论，
作为词条生产的参考素材。输出到 采集/采集/ 目录。
"""
import urllib.request, urllib.parse, json, socket, time, os, sys

socket.setdefaulttimeout(20)
PROXY = "http://127.0.0.1:7892"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def fetch(url, use_proxy=False, retry=3):
    for i in range(retry):
        try:
            if use_proxy:
                ph = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
                op = urllib.request.build_opener(ph)
            else:
                op = urllib.request.build_opener()
            req = urllib.request.Request(url, headers=UA)
            with op.open(req, timeout=25) as r:
                return r.read().decode('utf-8', errors='replace')
        except Exception as e:
            if i == retry - 1:
                return None
            time.sleep(2 * (i + 1))
    return None

def gh_search(q, per_page=8):
    url = f"https://api.github.com/search/issues?q={urllib.parse.quote(q)}&sort=reactions&order=desc&per_page={per_page}"
    d = json.loads(fetch(url) or "{}")
    out = []
    for it in d.get("items", []):
        out.append({
            "repo": it.get("repository_url", "").replace("https://api.github.com/repos/", ""),
            "title": it.get("title", ""),
            "url": it.get("html_url", ""),
            "reactions": (it.get("reactions") or {}).get("total_count", 0),
        })
    return out

def reddit_search(sub, q, limit=6):
    url = f"https://www.reddit.com/r/{sub}/search.json?q={urllib.parse.quote(q)}&restrict_sr=1&sort=top&t=year&limit={limit}"
    d = json.loads(fetch(url, use_proxy=True) or "{}")
    out = []
    for ch in d.get("data", {}).get("children", []):
        c = ch.get("data", {})
        out.append({
            "title": c.get("title", ""),
            "url": f"https://reddit.com{c.get('permalink','')}",
            "score": c.get("score", 0),
            "comments": c.get("num_comments", 0),
        })
    return out

OUT = r"D:\AIGC术语库\采集\采集"
os.makedirs(OUT, exist_ok=True)

def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 已存 {name}")

# ============ 采集任务 ============
print("=" * 50)
print("1. bf16 vs fp16 — GitHub 讨论")
r = gh_search("bf16 vs fp16 AMD")
save("bf16-fp16-github.md", "# bf16 vs fp16 社区讨论\n\n" + "\n".join(
    f"- [{x['repo']}] {x['title']} (👍{x['reactions']}) {x['url']}" for x in r))

print("2. RDNA2 int8 崩溃 — GitHub")
r = gh_search("RDNA2 int8 crash OR hipblas OR WMMA")
save("rdna2-int8-crash.md", "# RDNA2 int8/fp8 崩溃社区报告\n\n" + "\n".join(
    f"- [{x['repo']}] {x['title']} (👍{x['reactions']}) {x['url']}" for x in r))

print("3. LoRA vs 蒸馏 — Reddit")
r = reddit_search("StableDiffusion", "LoRA vs distilled turbo")
save("lora-vs-distill-reddit.md", "# LoRA vs 蒸馏 社区讨论 (r/StableDiffusion)\n\n" + "\n".join(
    f"- [{x['score']}分/{x['comments']}评] {x['title']} {x['url']}" for x in r))

print("4. GGUF 量化级别 — GitHub")
r = gh_search("GGUF Q4_K_M vs Q8")
save("gguf-quants.md", "# GGUF 量化级别讨论\n\n" + "\n".join(
    f"- [{x['repo']}] {x['title']} (👍{x['reactions']}) {x['url']}" for x in r))

print("5. 风格模型 Pony/animagine — Reddit")
r = reddit_search("StableDiffusion", "Pony vs animagine anime style")
save("style-models.md", "# 风格模型社区讨论\n\n" + "\n".join(
    f"- [{x['score']}分/{x['comments']}评] {x['title']} {x['url']}" for x in r))

print("6. Textual Inversion vs LoRA — GitHub")
r = gh_search("textual inversion vs LoRA")
save("textual-inversion.md", "# Textual Inversion vs LoRA\n\n" + "\n".join(
    f"- [{x['repo']}] {x['title']} (👍{x['reactions']}) {x['url']}" for x in r))

print("\n采集完成，输出目录:", OUT)
