# -*- coding: utf-8 -*-
"""构建产物断链校验。

扫描 dist 下所有 html，检查指向本站的链接是否都有对应的文件。
置于「四道闸门」的第三道：语义校验过了、页面也生成了，
但链接指错地方依然会让读者撞上 404。

用法（在仓库根执行）：

    python scripts/check_dist_links.py

退出码 0 = 无断链；非 0 = 存在断链，CI 据此拦截。
"""
import os
import re
import sys
import urllib.parse
from pathlib import Path

# 脚本在 scripts/ 下，仓库根是它的上一级 —— 这样换机器、换路径都不用改
REPO = Path(__file__).resolve().parent.parent
ROOT = REPO / 'dist'

# 与 src/lib/paths.mjs 里的 BASE 保持一致；换域名时两处一起改
BASE = '/ai-knowledge-base'

HREF = re.compile(r'(?:href|src)="([^"]+)"')


def target_exists(url_path: str) -> bool:
    p = url_path.split('#')[0].split('?')[0]
    if not p:
        return True
    p = urllib.parse.unquote(p).lstrip('/')
    # 目录式 URL（以 / 结尾或没有扩展名）找它的 index.html
    if p.endswith('/') or not os.path.splitext(p)[1]:
        return (ROOT / p / 'index.html').exists()
    return (ROOT / p).exists()


def main() -> int:
    if not ROOT.exists():
        print(f'找不到构建产物：{ROOT}')
        print('请先执行 npm run build')
        return 1

    pages = [h for h in ROOT.rglob('*.html') if 'pagefind' not in h.parts]
    checked = 0
    missing: dict[str, int] = {}

    for html in pages:
        text = html.read_text(encoding='utf-8', errors='replace')
        for m in HREF.finditer(text):
            u = m.group(1)
            if u != BASE and not u.startswith(BASE + '/'):
                continue
            checked += 1
            if not target_exists(u[len(BASE):]):
                missing[u] = missing.get(u, 0) + 1

    print(f'扫描页面: {len(pages)} 个')
    print(f'站内链接: {checked} 条')
    print(f'断链: {len(missing)} 条')
    for u, n in sorted(missing.items(), key=lambda kv: -kv[1])[:30]:
        print(f'  {n:>3}x  {u}')

    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main())
