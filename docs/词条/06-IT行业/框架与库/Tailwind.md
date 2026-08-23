---
term: Tailwind
full_name: Tailwind CSS
aliases: [原子化CSS, 实用类CSS]
category: 工具
dimension: 框架与库
granularity: 框架
maturity: stable
status: published
contributors: [TEXXXXTURE]
sources:
  - https://tailwindcss.com
relations:
  - target: React
    note: 最常见的搭配——React 项目用 Tailwind 写样式，AI 生成前端的事实标准组合
  - target: shadcn
    note: shadcn/ui 组件库构建在 Tailwind 之上
  - target: Vite
    note: Vite + Tailwind 是轻量前端工程的常见组合
created: 2026-08-23
updated: 2026-08-23
revisions: 1
---

## 定义

Tailwind CSS 是一个原子化（utility-first）CSS 框架：不写自定义 CSS 类，而是用 `flex`、`p-4`、`text-lg` 这类单一用途的类名直接组合样式。因为每个类只做一件事，样式写在 HTML 里，不需要在 CSS 文件里来回切换。

## 原理

Tailwind 用构建时扫描（content detection）找到源文件里出现的类名，只生成用到的样式，产物极小。类名体系靠设计令牌（design token）驱动——颜色、间距、圆角、字体全部走 `tailwind.config.js` 里的变量，改一个 token 全站生效。这套"令牌驱动"正是它成为 AI 生成前端标准的原因：模型只需要输出类名字符串，不需要理解复杂 CSS 层叠。

## 由来与历史

2020 年由 Adam Wathan 发布 v1，设计初衷是解决 Bootstrap 式"组件类"难以定制的问题。随着 shadcn/ui 等"复制粘贴组件"生态兴起，Tailwind 成为 AI 生成前端的默认选择——LLM 训练语料里它的类名出现频率最高，生成质量最稳定，这也是大量 AI 小软件界面趋同的底层原因。

## 应用

- 与 React/Next.js/Vue 搭配写界面，AI 生成质量最高的前端栈
- shadcn/ui、Radix UI 等现代组件库的样式基础
- 像素风等自定义风格：在 `tailwind.config.js` 里配自定义色板/字体即可，Token 化程度高

## 参见

- [React](React.md)
- [shadcn](shadcn.md)
- [Vite](Vite.md)
