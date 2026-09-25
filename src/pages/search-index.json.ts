import { getCollection } from 'astro:content';
import { termUrl } from '../lib/paths.mjs';

/** 顶栏即时搜索用的小索引：只有名字/别名/分类，几十 KB，首屏之外按需加载。 */
export async function GET() {
  const terms = await getCollection('terms');
  const payload = terms.map((e) => ({
    t: e.data.term,
    f: e.data.full_name ?? '',
    a: e.data.aliases ?? [],
    c: e.data.category ?? '',
    m: e.data.maturity,
    u: termUrl(e.id),
  }));

  return new Response(JSON.stringify(payload), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}
