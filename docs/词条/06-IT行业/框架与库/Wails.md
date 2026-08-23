---
term: Wails
full_name: Wails
aliases: []
category: 工具
dimension: 框架与库
granularity: 框架
maturity: hot
status: published
contributors: [TEXXXXTURE]
sources:
  - https://wails.io
  - https://github.com/wailsapp/wails
relations:
  - target: Tauri
    note: 同为轻量桌面框架，Wails 用 Go 后端，Tauri 用 Rust
  - target: Electron
    note: Electron 的轻量替代方案之一
created: 2026-08-23
updated: 2026-08-23
revisions: 1
---

## 定义

Wails 是一个用 Go 写后端、Web 技术写前端的桌面应用框架：前端渲染界面，Go 提供系统能力，两者通过绑定调用。与 Tauri 定位类似（轻量桌面框架），区别在后端语言是 Go 而不是 Rust。

## 原理

Wails 把 Go 函数暴露给前端调用（类似 Electron 的 IPC），用系统 WebView 渲染，不打包 Chromium，所以体积小。Go 的并发模型适合做代理、网络请求等系统逻辑。生态和成熟度比 Tauri 小，但 Go 开发者上手更快。

## 由来与历史

2021 年由 Lea Anthony 发起，目标是让 Go 开发者能用 Web 技术做桌面应用。社区规模中等，更新活跃度不如 Tauri，但在 Go 社区有稳定用户群。

## 应用

- Go 技术栈团队的桌面工具
- 需要 Go 并发能力的本地工具（代理、批量处理客户端）
- 前端层同样可配 React/Vue + Tailwind

## 参见

- [Tauri](Tauri.md)
- [Electron](Electron.md)
