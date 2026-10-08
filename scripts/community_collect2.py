"""社区采集脚本 v2 — 针对性采集
直接在相关仓库内搜 issues（相关性高），Reddit 用 .json 直连。
"""
import urllib.request, urllib.parse, json, socket, time, os

socket.setdefaulttimeout(20)
PROXY = "http://127.0.0.1:7892"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Windows/10.0"}

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

def gh_repo_issues(repo, q, per_page=8):
    url = f"https://api.github.com/search/issues?q=repo:{repo}+{urllib.parse.quote(q)}&sort=reactions&order=desc&per_page={per_page}"
    d = json.loads(fetch(url) or "{}")
    out = []
    for it in d.get("items", []):
        out.append(f"- [{it.get('title','')}] (👍{(it.get('reactions') or {}).get('total_count',0)}) {it.get('html_url','')}")
    return out

def reddit_search(sub, q, limit=6):
    url = f"https://www.reddit.com/r/{sub}/search.json?q={urllib.parse.quote(q)}&restrict_sr=1&sort=top&t=year&limit={limit}"
    d = json.loads(fetch(url, use_proxy=True) or "{}")
    out = []
    for ch in d.get("data", {}).get("children", []):
        c = ch.get("data", {})
        out.append(f"- [{c.get('score',0)}分/{c.get('num_comments',0)}评] {c.get('title','')} https://reddit.com{c.get('permalink','')}")
    return out

OUT = r"D:\AIGC术语库\采集\采集"
os.makedirs(OUT, exist_ok=True)

def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {name}: {len(content)} 字")

print("1. ComfyUI 仓库 — AMD/RDNA2 量化问题")
save("comfyui-amd-issues.md", "# ComfyUI AMD/RDNA2 讨论\n\n" + "\n".join(
    gh_repo_issues("Comfy-Org/ComfyUI", "AMD RDNA2 OR ROCm OR int8 OR fp8")))

print("2. llama.cpp — GGUF 量化级别对比")
save("llamacpp-gguf.md", "# llama.cpp GGUF 量化讨论\n\n" + "\n".join(
    gh_repo_issues("ggml-org/llama.cpp", "GGUF quant Q4_K_M quality")))

print("3. stable-diffusion-webui — LoRA 训练")
save("sdwebui-lora.md", "# A1111 LoRA 讨论\n\n" + "\n".join(
    gh_repo_issues("AUTOMATIC1111/stable-diffusion-webui", "LoRA training quality")))

print("4. ComfyUI — SageAttention / 加速")
save("comfyui-sage.md", "# ComfyUI SageAttention/加速讨论\n\n" + "\n".join(
    gh_repo_issues("Comfy-Org/ComfyUI", "sageattention OR sage attention")))

print("5. Reddit — LoRA vs 蒸馏（换 UA 重试）")
r = reddit_search("StableDiffusion", "LoRA distilled model", 8)
save("reddit-lora-distill.md", "# r/StableDiffusion: LoRA vs 蒸馏\n\n" + "\n".join(r))

print("6. Reddit — GGUF / 量化")
r = reddit_search("LocalLLaMA", "GGUF quant quality Q4 Q8", 8)
save("reddit-gguf.md", "# r/LocalLLaMA: GGUF 量化\n\n" + "\n".join(r))

print("\n完成")
