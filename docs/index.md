---
title: AI 知识库
---

<div class="hero">
  <h1>AI 知识库</h1>
  <div class="subtitle">一线知识的沉淀与导航站。每个词条是一个节点，关系是边——从根往下读是一条完整学习路径，从叶子跳入是速查。</div>
  <div class="prompt"><span class="path">ai-kb@latest:~$</span> tree --depth=1 --style=wiki<span class="cursor"></span></div>
</div>

<div class="kb-tree">
<span class="dir">├─ AI 基础</span>          <span class="cnt">(12)</span> 机器学习 · 深度学习 · 数学与统计<br>
<span class="dir">├─ 组件</span>              <span class="cnt">(08)</span> CLIP · Tokenizer · UNet · VAE<br>
<span class="dir">├─ 生成与多模态</span>      <span class="cnt">(27)</span> <span class="hl">量化格式 · 微调 · 加速 · 对齐 · 厂商 · 家族</span><br>
<span class="dir">├─ LLM 与语言模型</span>    <span class="cnt">(12)</span> 推理引擎 · RAG · 提示词 · 评测<br>
<span class="dir">├─ Agent 与智能体</span>    <span class="cnt">(09)</span> 框架 · ReAct · 多 Agent 协作<br>
<span class="dir">├─ 文章与引用</span>        <span class="cnt">(01)</span> 每日 AI 阅读索引<br>
<span class="dir">└─ 计算机基础</span>        <span class="cnt">(28)</span> 语言 · 系统 · 基础设施 · 框架
</div>

## 栏目导航

<div class="kb-nav">
  <a href="文章与引用/index.md">
    <span class="n-title">文章与引用 <span class="n-cnt">NEW</span></span>
    <span class="n-desc">每日 AI 资讯聚合与阅读索引——聚合摘要 + 判断线索，不写原文</span>
  </a>
  <a href="项目文档/map.md">
    <span class="n-title">AI 知识地图 <span class="n-cnt">map</span></span>
    <span class="n-desc">全站网状入口：广义 AI 知识树 + 当前目录对应</span>
  </a>
  <a href="词条/01-底层原理/神经网络.md">
    <span class="n-title">底层原理 <span class="n-cnt">01</span></span>
    <span class="n-desc">理解一切的根：神经网络 / Transformer / 扩散模型 / 量化</span>
  </a>
  <a href="词条/02-组件/UNet.md">
    <span class="n-title">组件 <span class="n-cnt">02</span></span>
    <span class="n-desc">模型的零件：CLIP / Tokenizer / VAE / 采样器</span>
  </a>
  <a href="词条/04-LLM工程/推理引擎.md">
    <span class="n-title">LLM 工程 <span class="n-cnt">04</span></span>
    <span class="n-desc">LLM 落地：推理引擎 / RAG / 提示词 / 模型评测</span>
  </a>
  <a href="词条/05-Agent工程/Agent 框架.md">
    <span class="n-title">Agent 工程 <span class="n-cnt">05</span></span>
    <span class="n-desc">智能体开发：框架 / 工具调用 / MCP / 多 Agent 协作</span>
  </a>
  <a href="词条/06-IT行业/编程语言/Python.md">
    <span class="n-title">IT 行业 <span class="n-cnt">06</span></span>
    <span class="n-desc">编程语言 / 操作系统 / 基础设施 / 框架与库</span>
  </a>
  <a href="词条/04-LLM工程/模型数据总览.md">
    <span class="n-title">模型数据总览 <span class="n-cnt">data</span></span>
    <span class="n-desc">28 模型 × 7 维度：智能指数 / 价格 / 速度 / 上下文 / 开放度</span>
  </a>
</div>

## 前沿采集

机器自动扫描社区（GitHub / arXiv / 讨论）生成的热词卡，未经沉淀、先看先得。见 `采集/` 目录。

## 项目文档

| 文档 | 是什么 |
|------|--------|
| [AI 知识地图](项目文档/map.md) | 全站网状入口：广义 AI 知识树 + 当前目录对应 |
| [PRD（人类版）](项目文档/PRD-人类版.md) | 项目是什么、框架、进度——快速了解 |
| [PRD（Agent 版）](项目文档/PRD-Agent版.md) | 完整设计决策 + 技术细节 + 踩坑记录 |
| [内容规范](项目文档/CONTENT-SPEC.md) | 词条长什么样、怎么写、怎么连线、怎么校验 |
| [贡献指南](项目文档/CONTRIBUTING.md) | 四层贡献模型：读者 / 贡献者 / 维护者 / 机器 |
| [维护流程](项目文档/MAINTENANCE.md) | 审校 / 发布 / 采集 / 升降级 / 回滚 |
| [设计定案](项目文档/DESIGN-SPEC.md) | 项目设计决策的唯一事实源 |

## 贡献

欢迎任何人参与！提 Issue 纠错、提 PR 写词条。仓库：[TEXXXXTURE/ai-knowledge-base](https://github.com/TEXXXXTURE/ai-knowledge-base)
