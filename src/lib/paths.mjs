// 全站唯一的位置与路径事实源：改这里，全站跟着变。
import { fileURLToPath } from 'node:url';

/** GitHub Pages 项目站点的基础路径，换自定义域名时改这里 */
export const BASE = '/ai-knowledge-base';

/** 词条目录（内容唯一来源，不搬家、不复制）——URL 形态，供 content loader 使用 */
export const TERM_ROOT_URL = new URL('../../docs/词条/', import.meta.url);

/** 项目文档目录——URL 形态 */
export const DOC_ROOT_URL = new URL('../../docs/项目文档/', import.meta.url);

/** 工具库目录（工具拆解，来自 tool-intel-wiki 并入）——URL 形态 */
export const TOOL_ROOT_URL = new URL('../../docs/工具库/', import.meta.url);

/** 情报日报目录（来自 tool-intel-wiki 并入）——URL 形态 */
export const DIGEST_ROOT_URL = new URL('../../docs/情报日报/', import.meta.url);

/** 文件系统路径形态，供 remark 插件等需要绝对路径的地方使用 */
export const TERM_ROOT = fileURLToPath(TERM_ROOT_URL);
export const DOC_ROOT = fileURLToPath(DOC_ROOT_URL);
export const TOOL_ROOT = fileURLToPath(TOOL_ROOT_URL);
export const DIGEST_ROOT = fileURLToPath(DIGEST_ROOT_URL);

/** 把词条 id（相对路径）转成站内 URL */
export function termUrl(id) {
  return `${BASE}/term/${id.split('/').map(encodeURIComponent).join('/')}/`;
}

/** 把分组 key 转成分类页 URL */
export function catUrl(key) {
  return `${BASE}/cat/${encodeURIComponent(key)}/`;
}

/** 把项目文档 id 转成文档页 URL */
export function docUrl(id) {
  return `${BASE}/doc/${id.split('/').map(encodeURIComponent).join('/')}/`;
}

/** 把工具拆解 id 转成工具页 URL */
export function toolUrl(id) {
  return `${BASE}/tool/${id.split('/').map(encodeURIComponent).join('/')}/`;
}

/** 把情报日报 id 转成日报页 URL */
export function digestUrl(id) {
  return `${BASE}/digest/${id.split('/').map(encodeURIComponent).join('/')}/`;
}
