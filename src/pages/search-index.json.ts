import { getCollection } from 'astro:content';
import { termUrl, toolUrl, digestUrl } from '../lib/paths.mjs';

/**
 * 顶栏即时搜索用的小索引：只有名字/别名/分类，几十 KB，首屏之外按需加载。
 *
 * 与 /search/（Pagefind 全文搜索）的分工：
 *   本文件 —— 「找名字」，输入即出，覆盖三个内容域
 *   Pagefind —— 「找正文」，回车后走全站全文索引
 * 所以这里收录不全不会漏内容，只是少了即时提示。
 */
export async function GET() {
  const [terms, tools, digests] = await Promise.all([
    getCollection('terms'),
    getCollection('tools'),
    getCollection('digests'),
  ]);

  const payload = [
    ...terms.map((e) => ({
      t: e.data.term,
      f: e.data.full_name ?? '',
      a: e.data.aliases ?? [],
      c: e.data.category ?? '',
      // 词条用 maturity（hot 加标记），另两域用 verified
      m: e.data.maturity,
      u: termUrl(e.id),
    })),
    ...tools.map((e) => ({
      t: e.data.title,
      f: e.data.summary ?? '',
      a: e.data.tags ?? [],
      c: '工具库',
      m: e.data.verified ? 'verified' : '',
      u: toolUrl(e.id),
    })),
    ...digests.map((e) => ({
      t: e.data.title,
      f: e.data.summary ?? '',
      a: e.data.tags ?? [],
      c: '情报日报',
      m: '',
      u: digestUrl(e.id),
    })),
  ];

  return new Response(JSON.stringify(payload), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}
