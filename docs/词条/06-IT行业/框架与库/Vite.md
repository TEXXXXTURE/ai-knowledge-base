---
term: Vite
full_name: Vite
aliases: [vite]
category: 工具
dimension: 框架与库
granularity: 构建工具
maturity: stable
status: published
contributors: [TEXXXXTURE]
sources:
  - https://vitejs.dev
  - https://github.com/vitejs/vite
relations:
  - target: React
    note: React 项目的事实标准构建工具（create-vite）
  - target: Electron
    note: electron-vite 是 Electron 前端构建的标准方案
  - target: Next.js
    note: 同为前端工程基础设施，Vite 面向 SPA，Next.js 面向 SSR
created: 2026-08-23
updated: 2026-08-23
revisions: 1
---

## 定义

Vite 是一个前端构建工具（bundler）：开发时秒级启动、热更新，生产时打包优化产物。它取代了 Webpack 成为 React/Vue 新项目的事实标准——`npm create vite` 是新建前端项目最常见的起点。

## 原理

Vite 开发模式基于原生 ES Modules：浏览器直接加载模块，不需要预打包，所以启动只要几百毫秒。生产构建用 Rollup 打包。核心价值是"快"——开发体验决定了它成为 AI 生成前端项目的默认脚手架（AI 输出的代码几乎都假设 Vite 环境）。

## 由来与历史

2020 年由 Vue 作者尤雨溪发布，最初是 Vue 的配套工具，后扩展为框架无关。2022 年前后取代 Webpack 成为主流选择，现在所有主流框架（React/Vue/Svelte/Solid）的官方脚手架都基于 Vite。electron-vite 则是 Electron 项目的标准构建方案。

## 应用

- React/Vue 项目脚手架（create-vite）
- Electron 项目构建（electron-vite，TabTin 用的就是这个）
- 静态站点/单页应用打包，配合 GitHub Pages 部署

## 参见

- [React](React.md)
- [Electron](Electron.md)
- [Next.js](Next.js.md)
