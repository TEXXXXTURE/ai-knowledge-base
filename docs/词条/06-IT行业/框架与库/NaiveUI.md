---
term: Naive UI
full_name: Naive UI
aliases: [NaiveUI]
category: 工具
dimension: 框架与库
granularity: 组件库
maturity: hot
status: published
contributors: [TEXXXXTURE]
sources:
  - https://www.naiveui.com
  - https://github.com/tusen-ai/naive-ui
relations:
  - target: Vue
    note: Vue 3 生态的主流组件库之一
  - target: AntDesign
    note: 常拿来对比的组件库，Naive UI 更轻更现代
  - target: shadcn
    note: 另一个可选的组件方案，shadcn 走复制粘贴，Naive UI 走开箱即用
created: 2026-08-23
updated: 2026-08-23
revisions: 1
---

## 定义

Naive UI 是一个 Vue 3 的组件库，提供按钮、表格、表单、弹窗等企业级组件，支持 TypeScript、主题定制和暗色模式。特点是"开箱即用"——安装后直接用，不需要像 shadcn 那样复制源码。

## 原理

基于 Vue 3 的组合式 API 构建，组件内部用 CSS 变量做主题令牌，通过 `n-config-provider` 统一配置主题。相比 Element Plus 更现代、更轻，相比 shadcn 的"复制粘贴"模式则是"包管理"模式——升级由库维护。

## 由来与历史

2021 年由社区项目（tusen-ai）发布，面向追求 TypeScript 体验和现代设计的 Vue 开发者。在中文社区流行度很高，是 Vue 3 项目的三大组件库之一（Element Plus / Naive UI / Ant Design Vue）。

## 应用

- Vue 3 项目的企业级界面
- Electron + Vue + Naive UI 是桌面工具的常用组合（国内 AI 小软件常见）
- 需要快速成型、不想自己维护组件源码的场景

## 参见

- [Vue](Vue.md)
- [Ant Design](AntDesign.md)
- [shadcn](shadcn.md)
