---
term: Tauri
full_name: Tauri
aliases: []
category: 工具
dimension: 框架与库
granularity: 框架
maturity: hot
status: published
contributors: [TEXXXXTURE]
sources:
  - https://tauri.app
  - https://github.com/tauri-apps/tauri
relations:
  - target: Electron
    note: 同为桌面应用框架，Tauri 是 Electron 的轻量替代
  - target: Wails
    note: 另一个轻量桌面框架，Wails 用 Go，Tauri 用 Rust
  - target: React
    note: 前端层可用任意 Web 框架，React 最常见
created: 2026-08-23
updated: 2026-08-23
revisions: 1
---

## 定义

Tauri 是一个用系统 WebView 渲染界面的桌面应用框架：前端用 Web 技术（React/Vue/Svelte 都行），后端用 Rust。与 Electron 最大的区别是它不打包 Chromium，而是调用操作系统自带的 WebView，安装包从 Electron 的 100MB+ 降到 5-10MB。

## 原理

Tauri 分两层：前端（WebView 渲染）+ 后端（Rust 核心进程）。两者通过 IPC 通信，前端调用 Rust 函数执行系统级操作。因为不捆绑浏览器引擎，内存占用和安装体积都显著低于 Electron。代价是不同系统 WebView 渲染有细微差异，且 Rust 学习曲线比 Node.js 陡。

## 由来与历史

2019 年由 Tauri 社区发起，目标是做"小而美"的 Electron 替代。2022 年发布 1.0，2024 年发布 2.0 支持移动端。随着用户对 Electron 应用体积和内存的抱怨增多，Tauri 成为桌面开发的新选择，但生态和成熟度仍不如 Electron。

## 应用

- 在意安装包体积/内存占用的桌面工具（如小体量 Agent 客户端）
- 前端层照用 React + Tailwind + shadcn，工程体验与 Electron 一致
- Rust 后端可做性能敏感的系统集成

## 参见

- [Electron](Electron.md)
- [Wails](Wails.md)
- [React](React.md)
