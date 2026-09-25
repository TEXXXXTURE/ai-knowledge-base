// 把词条正文里的相对 Markdown 链接（](神经网络.md)）改写为站内路由。
// 词条之间用手写相对路径互链是现有仓库的既成事实，这里一次性把它翻译成 URL。
import path from 'node:path';
import { slug as githubSlug } from 'github-slugger';
import { visit } from 'unist-util-visit';

const EXTERNAL = /^[a-z][a-z0-9+.-]*:/i;

export default function remarkTermLinks(options = {}) {
  const { termRoot, docRoot, base = '', termPrefix = '/term', docPrefix = '/doc' } = options;

  return (tree, file) => {
    const filePath = file?.path || file?.history?.[0];
    if (!filePath) return;
    const dir = path.dirname(filePath);

    visit(tree, 'link', (node) => {
      const url = node.url;
      if (!url || EXTERNAL.test(url) || url.startsWith('#') || url.startsWith('/')) return;

      const [rawPath, hash = ''] = url.split('#');
      if (!/\.md$/i.test(rawPath)) return;

      const abs = path.resolve(dir, safeDecode(rawPath));
      const suffix = hash ? `#${hash}` : '';

      const inTerms = toRelative(termRoot, abs);
      if (inTerms) {
        node.url = `${base}${termPrefix}/${encodePath(inTerms)}/${suffix}`;
        return;
      }

      const inDocs = toRelative(docRoot, abs);
      if (inDocs) {
        node.url = `${base}${docPrefix}/${encodePath(inDocs)}/${suffix}`;
        return;
      }

      // 彻底跑出 docs 之外：原样保留，交给构建后的人工排查
    });
  };
}

function toRelative(root, abs) {
  if (!root) return null;
  const rel = path.relative(root, abs).replace(/\\/g, '/');
  if (!rel || rel.startsWith('..')) return null;
  return rel.replace(/\.md$/i, '');
}

// 必须和 Astro glob loader 生成 entry.id 的算法逐字一致，否则正文链接会 404。
// Astro 的实现（node_modules/astro/dist/content/utils.js）：
//   const slug = rawSlugSegments.map((segment) => githubSlug(segment)).join("/")
// 差异会立刻显形：llama.cpp -> llamacpp、TextualInversion -> textualinversion。
// GitHub Pages 跑在大小写敏感的 Linux 上，大小写不统一 = 线上 404。
function encodePath(rel) {
  return rel
    .split('/')
    .map((segment) => encodeURIComponent(githubSlug(segment)))
    .join('/');
}

function safeDecode(s) {
  try {
    return decodeURIComponent(s);
  } catch {
    return s;
  }
}
