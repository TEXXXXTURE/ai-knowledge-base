---
term: IP-Adapter
full_name: Image Prompt Adapter
aliases: [图像提示适配器, 图像条件注入]
category: 多模态
dimension: 语义注入技术
granularity: 具体技术
maturity: hot
status: published
contributors: [TEXXXXTURE]
sources:
  - https://arxiv.org/abs/2308.06721
  - https://github.com/tencent-ailab/IP-Adapter
  - https://github.com/cubiq/ComfyUI_IPAdapter_plus
relations:
  - type: applies_to
    target: CLIP
    note: IP-Adapter 用 CLIP 图像编码器提取参考图特征
  - target: 风格模型
    note: 语义层面的风格迁移可与风格模型叠加使用
  - target: 扩散模型
    note: IP-Adapter 在扩散模型去噪过程中注入图像条件，不改权重
  - target: Textual Inversion
    note: 同属「不动模型权重」的轻量语义注入路线
  - type: contrast
    target: ControlNet
    note: 同为条件注入，ControlNet 管结构、IP-Adapter 管语义
created: 2026-08-14
updated: 2026-08-14
revisions: 1
---

## 定义

[热词] 社区热词，未经沉淀，信息可能快速过时

IP-Adapter（Image Prompt Adapter，图像提示适配器）是一种图像条件注入技术，一句话说清：不用文字、直接用一张参考图当「提示词」——把它喂给模型，就能在不动任何模型权重的情况下，让生成结果继承参考图的角色长相或画风。它是图生图、风格迁移、角色一致性工作流的核心组件。

## 原理

参考图先经 CLIP 图像编码器提取特征，再通过一组额外训练的、与文本条件**解耦**的交叉注意力层注入去噪网络——模型原有的文字提示通路完全不受影响，两条通路各管各的。因为它只加适配层、不改权重，同一个 IP-Adapter 可以即插即拔。背景见[CLIP](../../02-组件/CLIP.md)与[扩散模型](../../01-底层原理/扩散模型.md)。

## 由来与历史

2023 年 8 月，腾讯 AI Lab 发表 IP-Adapter 论文（arXiv:2308.06721）并开源。它把「图像提示」这件事从整模微调（DreamBooth 路线）变成了轻量的插件路线，很快在 ComfyUI 生态普及——cubiq 的 ComfyUI_IPAdapter_plus 成为事实标准实现。此后 FaceID、InstantID 等专注人脸一致性的变体相继出现。由于它依赖 CLIP 图像编码器，而新一代模型（SD3、FLUX、Z-Image）纷纷改用其他文本/视觉编码器，IP-Adapter 对新架构的适配始终慢半拍、方案仍在快速演进——这是本条目标 hot 的原因。

## 应用

ComfyUI 里通过 **ComfyUI_IPAdapter_plus** 插件使用：需要 IPAdapter 模型文件（`models/ipadapter/`）+ 配套的 CLIP Vision 模型（`models/clip_vision/`），核心节点是 IPAdapterAdvanced，`weight` 参数控制参考图影响力（0.5 左右起步，拉满容易过拟合参考图）。

典型场景与注意事项：

- **角色一致性**：喂一张角色图，批量生成同一角色不同姿势/场景，比训 LoRA 快得多但一致性略弱。
- **风格迁移**：喂画风参考图，配合较低的 weight 做语义级风格借鉴。
- **与 ControlNet 的分工**：IP-Adapter 管语义（画什么内容、什么风格），ControlNet 管结构（姿态、线稿、深度），两者常叠加使用，互不冲突。

## 争议 / 讨论

- **版权问题**：用他人作品当参考图做风格迁移，边界比风格模型更模糊——模型没学过这张图，但输出明显受它引导。
- **新架构适配滞后**：Z-Image 这一代模型换了文本编码器，社区 IP-Adapter 方案的稳定性与效果仍在打磨，使用前请确认对应模型家族的适配进度。

## 参见

- [CLIP](../../02-组件/CLIP.md)
- [扩散模型](../../01-底层原理/扩散模型.md)
- [Textual Inversion](TextualInversion.md)
- [ControlNet](../多模态/ControlNet.md)
- [风格模型](../微调/风格模型.md)
