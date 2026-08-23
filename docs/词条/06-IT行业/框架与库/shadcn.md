---
term: shadcn
full_name: shadcn/ui
aliases: [shadcn UI]
category: 工具
dimension: 框架与库
granularity: 组件库
maturity: hot
status: published
contributors: [TEXXXXTURE]
sources:
  - https://ui.shadcn.com
  - https://github.com/shadcn-ui/ui
relations:
  - target: Tailwind
    note: 组件全部用 Tailwind 类构建，样式可定制
  - target: React
    note: 基于 React + Radix UI 的无头组件构建
  - target: AntDesign
    note: 常拿来对比的另一类组件库——shadcn 是复制粘贴模式，AntD 是开箱即用
  - target: Next.js
    note: 官方推荐的 Next.js 搭配，SaaS 产品标配
created: 2026-08-23
updated: 2026-08-23
revisions: 1
---

## 定义

shadcn/ui 是一套"复制粘贴式"的 React 组件库：不是 npm 安装后直接用，而是把组件源码复制进你自己的项目，随你修改。它提供按钮、卡片、对话框、下拉菜单等常用组件，底层用 Radix UI 的无头组件保证可访问性，样式用 Tailwind 写。

## 原理

区别于传统组件库的"封装模式"，shadcn 走"拥有源码"模式：组件代码属于你的项目，不受库版本升级绑架，可以任意改样式和逻辑。所有组件用 CSS 变量（design token）定义主题，换主题色就是改几个变量。这套设计让它成为 AI 生成前端的"默认皮肤"——模型见过最多、生成最准。

## 由来与历史

2023 年由 shadcn（本名 Shu Ding）发布，迅速成为 React 生态最流行的组件方案。它踩中了 AI 编程时代的痛点：组件要可改、可定制、可被 LLM 生成。GitHub 星标增长极快，Vercel 系产品（Next.js 生态）大量采用。

## 应用

- 自研工具型桌面/Web 应用（如 Agent 工作台）的默认 UI 方案
- Next.js + Tailwind + shadcn 是 AI SaaS 产品三件套
- 桌面端用 Electron 壳 + 这套前端栈，就是 TabTin 等产品的实际架构

## 参见

- [Tailwind](Tailwind.md)
- [React](React.md)
- [Next.js](Next.js.md)
- [Ant Design](AntDesign.md)
