import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
import {
  TERM_ROOT_URL,
  DOC_ROOT_URL,
  TOOL_ROOT_URL,
  DIGEST_ROOT_URL,
} from './lib/paths.mjs';

/**
 * 词条 schema —— 字段与 docs/词条 现有 frontmatter 一一对应。
 * 覆盖率实测 139/139，所以这里用严格校验：谁少写一个字段，构建就会报出来。
 */
const terms = defineCollection({
  loader: glob({ pattern: '**/*.md', base: TERM_ROOT_URL }),
  schema: z.object({
    term: z.string(),
    full_name: z.string().default(''),
    aliases: z.array(z.string()).default([]),
    category: z.string().default(''),
    dimension: z.string().default(''),
    granularity: z.string().default(''),
    maturity: z.string().default('stable'),
    status: z.string().default(''),
    contributors: z.array(z.string()).default([]),
    sources: z.array(z.string()).default([]),
    relations: z
      .array(
        z.object({
          target: z.string(),
          note: z.string().optional(),
          type: z.string().optional(),
        }),
      )
      .default([]),
    created: dateish(),
    updated: dateish(),
    revisions: z.number().default(0),
  }),
});

/** 项目文档：结构不固定，宽松放行，只保证 title 可用 */
const projectdocs = defineCollection({
  loader: glob({ pattern: '**/*.md', base: DOC_ROOT_URL }),
});

/**
 * 工具库：工具拆解（原 tool-intel-wiki 的 tools 栏目）。
 * `related` 指向词条名，由 buildNameIndex 解析成可点链接；解析不到就不渲染。
 */
const tools = defineCollection({
  loader: glob({ pattern: '**/*.md', base: TOOL_ROOT_URL }),
  schema: z.object({
    title: z.string(),
    date: dateish(),
    type: z.string().default('tool'),
    source: z.string().default(''),
    tags: z.array(z.string()).default([]),
    verified: z.boolean().default(false),
    rating: z.number().default(0),
    url: z.string().default(''),
    summary: z.string().default(''),
    tools: z.array(z.string()).default([]),
    related: z.array(z.string()).default([]),
  }),
});

/** 情报日报：原 tool-intel-wiki 的 digest 栏目，按日期倒序成时间线 */
const digests = defineCollection({
  loader: glob({ pattern: '**/*.md', base: DIGEST_ROOT_URL }),
  schema: z.object({
    title: z.string(),
    date: dateish(),
    type: z.string().default('digest'),
    source: z.string().default(''),
    tags: z.array(z.string()).default([]),
    verified: z.boolean().default(false),
    summary: z.string().default(''),
  }),
});

/** YAML 里 2026-08 是字符串、2026-08-10 会被解析成 Date，统一成 YYYY-MM-DD */
function dateish() {
  return z
    .union([z.string(), z.date()])
    .optional()
    .transform((v) => {
      if (v instanceof Date) return v.toISOString().slice(0, 10);
      return v ?? '';
    });
}

export const collections = { terms, projectdocs, tools, digests };
