# 「文章与引用」栏目调研 — MOKE AIGC

> 日期：2026-08-14 ｜ 状态：调研完成，待实施
> 来源：https://www.mokeaigc.com/tutorial.html

## 目标站分析

**MOKE AIGC · Creative Studio** —— 小红书/抖音/X 上的 AIGC 创作者（MOKEAIGC），做的是一个「每日 AI 阅读索引」。

### 技术结构（爬取模式评估）

- **纯静态 SPA**：内容硬编码在 JS bundle（zcdn.rytesa.cn/moke-v3/*/runtime/inline/index-1.js），无后端 API
- **爬取模式**：抓 JS bundle → 正则提取 `article\w+: "..."` 字段（标题/日期/正文/标签）
- **验证**：23 个字段全部正则可提取，零反爬（CDN 直接放行）

### 站内栏目结构

| 栏目 | 内容 |
|------|------|
| 视觉板块（Visual） | 作品展示 |
| 技术与资讯（Tech & Intel） | 每日阅读索引 |
| Skill 提示词库（Prompt Library） | 150 电影技法 + 200 胶片 |
| 教程（Tutorial） | 教学 |

### 文章样例（「技术与资讯」栏目）

1. **Generative video is moving into controllable production**
   - 主题：视频模型 / 参考帧 / 一致性控制
2. **ClaudeCode and MCP are reshaping the creative tech stack**
   - 主题：Claude Code / MCP / 浏览器控制 / 本地脚本
3. **Cinematic techniques and film stocks**
   - 主题：电影技法 / 胶片库

### 核心模式提炼（值得借鉴）

MOKE 的模式 = **「聚合摘要 + 判断线索 + 阅读索引」**：
- 不写长篇原文，给「判断线索」（judgment cues）
- 聚合多家来源，做「阅读索引」（reading index）
- 声明免责（"provides aggregation summaries, judgment cues and reading indexes only"）

## 对我们的「文章与引用」栏目

### 定位建议

在 AIGC 术语知识库加一个「文章与引用」栏目，模式：

```
docs/文章与引用/
├── index.md          ← 索引页（每日/每周更新）
├── 聚合/
│   └── YYYY-MM-DD.md ← 当日 AI 资讯聚合（来源+摘要+判断线索）
└── 引用库/
    ├── 论文.md        ← 高质量论文引用（arXiv）
    └── 文章.md        ← 高质量文章引用（博客/官方）
```

### 采集模式（借鉴 MOKE + 复用现有素材库）

1. **人工聚合**（像 MOKE）：每篇引用 = 标题 + 来源 + 摘要 + 判断线索（一句话观点），不搬运全文
2. **雷达自动化**（我们已有）：cron 扫 arXiv/GitHub/HF → 自动生成热词卡 → 升级为引用条目
3. **与词条打通**：引用条目关联到词条（relations），词条页「参见」里出现引用

### 差异点（我们比 MOKE 强的地方）

- MOKE 是**单向输出**（他写你看）；我们是**开源协作**（贡献者能加引用）
- MOKE 无词条体系；我们的引用可以**挂到知识树上**（引用是词条的证据层）
- 我们的来源可验证（每个引用带原始 URL，CI 校验死链）

## 实施步骤（待用户确认）

1. 建 `docs/文章与引用/` 目录 + 索引页模板
2. 写采集脚本（复用 `scripts/community_collect2.py` 的抓取能力）
3. 首批 5-10 条引用（用素材库已有来源 + 社区采集结果）
4. 与词条 relations 打通
