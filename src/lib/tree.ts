import type { CollectionEntry } from 'astro:content';

/**
 * 侧栏目录树 —— 从文件目录结构自动长出来。
 * 这里是原先那份 139 行手工维护的 nav 的替代品：新增词条只要丢文件，导航自己更新。
 */

/** 分组显示名覆盖表。没写的分组会退化成「去掉数字前缀的文件夹名」。 */
const GROUP_LABEL: Record<string, string> = {
  '01-底层原理': '底层原理',
  '02-组件': '组件',
  '03-表层概念': '表层概念',
  '04-LLM工程': 'LLM 工程',
  '05-Agent工程': 'Agent 工程',
  '06-IT行业': '计算机基础',
};

/** 每层的一句话说明，首页「本期要目」用 */
export const GROUP_BLURB: Record<string, string> = {
  '01-底层原理': '数学与架构的地基',
  '02-组件': '模型内部的零件',
  '03-表层概念': '看得见、叫得出名字的那些',
  '04-LLM工程': '把它真正跑起来',
  '05-Agent工程': '从问答到能干活',
  '06-IT行业': '绕不开的计算机常识',
};

export type TermRef = {
  id: string;
  term: string;
  maturity: string;
  category: string;
  fullName: string;
};

export type SubNode = { name: string; terms: TermRef[] };

export type GroupNode = {
  key: string;
  num: string;
  label: string;
  blurb: string;
  count: number;
  terms: TermRef[];
  subs: SubNode[];
};

export type TermEntry = CollectionEntry<'terms'>;

export const groupKeyOf = (id: string) => id.split('/')[0];

export const subgroupOf = (id: string) => {
  const seg = id.split('/');
  return seg.length > 2 ? seg.slice(1, -1).join(' / ') : '';
};

export const groupLabel = (key: string) =>
  GROUP_LABEL[key] ?? key.replace(/^\d+-/, '');

export function toRef(e: TermEntry): TermRef {
  return {
    id: e.id,
    term: e.data.term,
    maturity: e.data.maturity,
    category: e.data.category,
    fullName: e.data.full_name,
  };
}

const byChinese = (a: TermRef, b: TermRef) => a.term.localeCompare(b.term, 'zh');

export function buildTree(entries: TermEntry[]): GroupNode[] {
  const byGroup = new Map<string, TermEntry[]>();
  for (const e of entries) {
    const key = groupKeyOf(e.id);
    const bucket = byGroup.get(key);
    if (bucket) bucket.push(e);
    else byGroup.set(key, [e]);
  }

  return [...byGroup.keys()].sort().map((key) => {
    const list = byGroup.get(key)!;
    const flat: TermRef[] = [];
    const subMap = new Map<string, TermRef[]>();

    for (const e of list) {
      const sub = subgroupOf(e.id);
      if (!sub) {
        flat.push(toRef(e));
        continue;
      }
      const bucket = subMap.get(sub);
      if (bucket) bucket.push(toRef(e));
      else subMap.set(sub, [toRef(e)]);
    }

    flat.sort(byChinese);
    const subs = [...subMap.entries()]
      .sort((a, b) => a[0].localeCompare(b[0], 'zh'))
      .map(([name, terms]) => ({ name, terms: terms.sort(byChinese) }));

    return {
      key,
      num: key.split('-')[0],
      label: groupLabel(key),
      blurb: GROUP_BLURB[key] ?? '',
      count: list.length,
      terms: flat,
      subs,
    };
  });
}

/** 名称 / 英文名 / 别名 → 词条 id，用于把 relations.target 变成可点的链接 */
export function buildNameIndex(entries: TermEntry[]): Map<string, string> {
  const map = new Map<string, string>();
  for (const e of entries) {
    if (!map.has(e.data.term)) map.set(e.data.term, e.id);
    for (const a of e.data.aliases) if (!map.has(a)) map.set(a, e.id);
  }
  return map;
}
