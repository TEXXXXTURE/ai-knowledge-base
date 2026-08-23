---
term: Ant Design
full_name: Ant Design
aliases: [antd]
category: 工具
dimension: 框架与库
granularity: 组件库
maturity: stable
status: published
contributors: [TEXXXXTURE]
sources:
  - https://ant.design
  - https://github.com/ant-design/ant-design
relations:
  - target: React
    note: React 生态最老牌的企业级组件库
  - target: NaiveUI
    note: 另一个组件库选择，AntD 更重更全，Naive UI 更轻
  - target: shadcn
    note: 新一代组件方案，shadcn 走可定制路线，AntD 走开箱即用
created: 2026-08-23
updated: 2026-08-23
revisions: 1
---

## 定义

Ant Design（antd）是 React 生态最老牌的企业级组件库，由蚂蚁集团开源，提供完整的后台管理界面组件：表格、表单、布局、图表、权限等。定位是"企业级中后台"——组件全、规范强、开箱即用。

## 原理

组件用 React 构建，主题通过 less 变量和 CSS-in-JS（新版本）定制。设计体系（Design Tokens）非常完整——色板、间距、字体、圆角都有官方规范。缺点是对应"企业后台"的视觉语言较重，改造成像素风等个性化风格需要覆盖大量默认样式。

## 由来与历史

2015 年由蚂蚁金服开源，是中文互联网中后台的事实标准，国内大量管理系统用它。React 16 时代它是默认选择；随着 shadcn 等新一代可定制方案出现，它在 AI 生成场景的份额被分流，但企业场景依然强势。

## 应用

- 企业中后台管理系统
- React 项目的快速成型（组件最全）
- 需要标准、规范、组件覆盖面的场景；追求个性化风格时慎用

## 参见

- [React](React.md)
- [Naive UI](NaiveUI.md)
- [shadcn](shadcn.md)
