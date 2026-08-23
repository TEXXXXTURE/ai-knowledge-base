---
term: Astro
full_name: Astro
aliases: []
category: 工具
dimension: 框架与库
granularity: 框架
maturity: hot
status: published
contributors: [TEXXXXTURE]
sources:
  - https://astro.build
  - https://github.com/withastro/astro
relations:
  - target: Next.js
    note: 同为内容型网站框架，Astro 主打零 JS 静态输出，Next.js 主打全栈
  - target: Vite
    note: Astro 构建在 Vite 之上
created: 2026-08-23
updated: 2026-08-23
revisions: 1
---

## 定义

Astro 是一个面向内容型网站的前端框架：默认输出零 JavaScript 的纯静态页面，需要交互时才按需注入组件（Islands 架构）。适合博客、文档站、知识库这类以内容为主的站点。

## 原理

Astro 的核心理念是"默认零 JS"——页面在构建时渲染成纯 HTML，交互组件（Islands）单独打包按需加载。支持在页面里混用 React/Vue/Svelte 组件。相比 Next.js 的全栈 SSR，Astro 更轻、更快，但不适合复杂应用逻辑。

## 由来与历史

2021 年发布，2022 年爆火，成为内容站/文档站的热门选择。MkDocs 生态外的另一条文档站路线（Astro Starlight 主题即官方文档方案）。

## 应用

- 博客、文档、知识库、个人主页
- 需要静态部署（GitHub Pages/Vercel）的内容站点
- 与 React 组件混用，渐进增强

## 参见

- [Next.js](Next.js.md)
- [Vite](Vite.md)
