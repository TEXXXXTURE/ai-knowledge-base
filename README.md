<div align="center">

<img src="public/mark.svg" width="76" height="76" alt="星图 ASTERISM">

# 星图 ASTERISM

**一线知识的沉淀与导航站**

没有数据库，只有一张表格。<br>
没有自动抓取，每一条都经人工筛选。

<sub>概念库 · 工具库 · 情报日报 · 项目文档</sub>

</div>

---

**目录**

1. [这是什么](#what)
2. [四根柱子](#pillars)
3. [目录结构](#tree)
4. [两层内容粒度](#layers)
5. [数据层](#data)
6. [本地开发](#dev)
7. [内容规范与校验](#spec)
8. [怎么贡献](#contribute)
9. [站点与关联](#links)

---

<a id="what"></a>

## 这是什么

**星图（ASTERISM）是一个把知识讲清楚的地方。** 当前以 AI 领域为主体，架构上支持扩展到任意知识领域。

从根往下读，是一条完整的学习路径；从叶子跳入，是速查。每个词条是独立页面，词条之间互相链接 —— 像一张不断生长、开放给所有人编写的知识星图。

### 两件要说在前头的事

**一、数据在一张表格里，不在数据库里。**

网站是纯静态的，构建即成品：没有服务器、没有 SQL、没有运维。唯一带结构的一层是**飞书多维表格**（三张表：词条 / 关系 / 投稿），它承担筛选、权限与审批 —— 这些恰恰是 Markdown 文件给不了的能力。

**二、每一条都经人工筛选，不是自动抓的。**

内容来自公开的视频、文章与社区讨论，经一套自建工作流汇集，再由人逐条过筛、确认值得留下才入库。**没有一条是自动灌进来的。** 所以这里的条目数不会暴涨，只会一点点长。

> 仓库名仍是 `ai-knowledge-base`（改名要动 Pages 路径与全站链接），对外名称与标识为 **星图 ASTERISM**。

全站网状入口见 [AI 知识地图](docs/项目文档/map.md)，整体设计见[设计说明页](https://texxxxture.github.io/ai-knowledge-base/design/)。

---

<a id="pillars"></a>

## 四根柱子

| 柱子 | 含义 | 靠什么撑住 |
|---|---|---|
| **上限** | 内容能多深、多新、多一线 | 来源层级 —— 每条都有原始链接 |
| **标准** | 多规范、多可信、多一致 | Schema 校验 + 无源不收录 |
| **生态** | 内容产品活着 | 开放编写 —— 四层贡献模型 |
| **信任** | 读者凭什么信 | Git 留痕 + 来源标注 + 修订记录 |

---

<a id="tree"></a>

## 目录结构

```
ai-knowledge-base/
├── docs/                     内容源头（唯一事实源）
│   ├── 词条/                 概念库，按六大领域分层
│   │   ├── 01-底层原理         Transformer / MoE / 量化 / 训练…
│   │   ├── 02-组件            CLIP / VAE / Tokenizer…
│   │   ├── 03-表层概念         Agent / LLM / 多模态 / 模型厂商…
│   │   ├── 04-LLM工程         推理优化 / RAG / 评测…
│   │   ├── 05-Agent工程       Agent 框架 / 工具调用 / 记忆…
│   │   └── 06-IT行业          基础设施 / 语言 / 框架…
│   ├── 工具库/                工具拆解（并入自 tool-intel-wiki）
│   ├── 情报日报/              工具情报官流水线的每日产出
│   ├── 文章与引用/            外部文章聚合与引用库
│   └── 项目文档/              PRD / 内容规范 / 设计规范 / 生产流程
├── 雷达/                     社区感知层：原始素材 → 采集表 → 热词卡
├── scripts/                  采集与维护脚本
│   └── validate_content.py   语义校验（CI 闸门）
├── src/                      Astro 前端
│   ├── pages/                词条 / 分类 / 工具 / 日报 / 搜索 / 设计说明
│   ├── components/           顶栏 / 侧栏
│   ├── layouts/              基础版式
│   └── lib/                  路径事实源 / 目录树 / remark 插件
└── ROADMAP.md                更新路径
```

**一条约定**：`src/lib/paths.mjs` 是全站唯一的位置事实源。要改目录名或换域名，改它一处，全站跟着变。

---

<a id="layers"></a>

## 两层内容粒度

知识不是一次成型的。有些已经想清楚、能独立成篇；有些还是半句话、一个线索。这里不硬把两者塞进同一层：

- **概念库（`docs/词条/`）** —— 沉淀层。成熟词条独立成页，按领域归类，通过 `relations` 连成知识网。
- **素材层（`docs/工具库/`、`docs/情报日报/`、`雷达/`）** —— 感知层。工具拆解、日报、社区热词。特点是**先记下来，再慢慢转正**：允许粗糙、允许存疑，但状态标清楚。

工具与日报之所以不塞进词条树，是因为它们的证据形态不同 —— 工具带验证状态与推荐度，日报带日期与来源视频。它们平级并存，靠「关联词条」字段挂回关系网。

---

<a id="data"></a>

## 数据层

**没有传统数据库。** 网站本身不需要 —— Markdown 加 Git 就够。但当 Agent 要改、外部读者要投稿时，文件就不够用了：没有筛选、没有权限、没有审批流。

补上这块的不是 MySQL 或 Postgres，而是**飞书多维表格**：一个本来就在用的协作工具，顺手当数据层。三张表 —— 词条表、关系表、投稿表。

**为什么关系要拆成独立的表**：词条里的 `relations` 是嵌套对象数组，而多维表格没有嵌套类型。塞进一个单元格是存得住，但从此查不了图 —— 问不出「谁是枢纽」「谁是孤岛」「两跳邻居有哪些」。拆成边表之后，这些都是一句话的查询。

数据层始终是**镜像**，不是源头。内容只在 `docs/` 里诞生。

---

<a id="dev"></a>

## 本地开发

需要 Node 18+。

```bash
npm install
npm run dev       # 开发服务器 → http://localhost:4321/ai-knowledge-base/
npm run build     # 构建静态站 + Pagefind 索引
npm run preview   # 预览构建产物
```

> **改了 remark 插件或内容 Schema 之后**，必须清掉内容层缓存再构建，否则部分页面会沿用旧渲染产物：
> `rm -rf .astro node_modules/.astro && npm run build`

技术栈：Astro + Content Collections + Pagefind。部署走 GitHub Pages（见 `.github/workflows/deploy.yml`）。

> **`package.json` 里那两个 `*-linux-x64-gnu` 可选依赖不要删。**
> npm 写锁文件时会剪掉「非当前平台」的 optional dependencies（[npm/cli#4828](https://github.com/npm/cli/issues/4828)），
> 于是在 Windows 上生成的 `package-lock.json` 不含 Linux 原生二进制，而 CI runner 是 Linux ——
> `npm ci` 严格照锁文件安装，会缺 `@astrojs/compiler-binding-linux-x64-gnu` 与 `lightningcss-linux-x64-gnu` 而构建失败。
> 登记成根级可选依赖后 npm 必须写进锁文件，Windows 本地则因 `os` 不匹配自动跳过（不占空间）。

---

<a id="spec"></a>

## 内容规范与校验

写词条前请先读 [CONTENT-SPEC.md](docs/项目文档/CONTENT-SPEC.md)（词条 Schema + 写作风格 + 成熟度分级 + 校验清单）。

校验分三道，改动会在不同环节被拦下：

| 闸门 | 位置 | 拦什么 |
|---|---|---|
| 类型 | `src/content.config.ts` | 字段类型与形状不对 → 构建失败 |
| 语义 | `scripts/validate_content.py` | 词条名重复、关系边指向不存在的词条、published 缺来源、枚举非法 |
| 链接 | `scripts/check_dist_links.py` | 构建产物里的站内断链（需先 `npm run build`） |

语义校验按 `status` 分级 —— published 必须有来源，draft 允许无来源。所以骨架词条可以先立框架，不会卡住 CI。

---

<a id="contribute"></a>

## 怎么贡献

欢迎任何人参与，详见 [CONTRIBUTING.md](docs/项目文档/CONTRIBUTING.md)。

四层贡献模型：

- **L1 读者** —— 提 Issue（纠错 / 补充 / 讨论）
- **L2 贡献者** —— 提 PR（提交词条草稿，过 Schema 校验后发布）
- **L3 维护者** —— 审校 / 合并 / 定稿
- **L4 机器** —— 雷达 Agent 自动抓热词卡

---

<a id="links"></a>

## 站点与关联

**名称**：星图 ASTERISM（仓库名与站点路径仍为 `ai-knowledge-base`）

**站点**：https://texxxxture.github.io/ai-knowledge-base/

**接下来做什么**：见 [ROADMAP.md](ROADMAP.md)。

**关联项目**：

- [工具情报官 Wiki](https://github.com/TEXXXXTURE/tool-intel-wiki) —— 内容已并入本站「工具库 / 情报日报」两个栏目
- [分布式 Agent 集群规则](https://github.com/TEXXXXTURE/distributed-agent-cluster-rules) —— 集群运行规则

**许可**：见 [LICENSE](LICENSE)
