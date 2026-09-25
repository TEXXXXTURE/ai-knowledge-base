---
term: LoRA
full_name: Low-Rank Adaptation
aliases: [低秩适配, lora]
category: 模型微调
dimension: 微调技术
granularity: 具体技术
maturity: stable
status: published
contributors: [TEXXXXTURE]
sources:
  - https://arxiv.org/abs/2106.09685
  - https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/13952
  - https://huggingface.co/learn/diffusion-course/unit2/1
relations:
  - type: part_of
    target: 训练与微调
    note: LoRA 是参数高效微调的一种实现
  - target: 蒸馏与Turbo
    note: 加速 LoRA（如 Turbo-LoRA、LCM-LoRA）是蒸馏成果的补丁形态
  - type: applies_to
    target: 风格模型
    note: 风格模型大多靠 LoRA 实现，也可做全量 checkpoint
  - type: contrast
    target: Textual Inversion
    note: 常被对比的另一种轻量个性化方案，LoRA 学「怎么画」
created: 2026-08-14
updated: 2026-08-14
revisions: 1
---

## 定义

LoRA（Low-Rank Adaptation，低秩适配）是微软 2021 年提出的微调技术，一句话说清：不动原模型的几十亿参数，只在每一层旁边挂一对很小的矩阵去学「变化量」，产物是一个几十 MB 的补丁文件。在图像生成社区，LoRA 几乎成了「微调」的代名词——画风、角色、构图、甚至加速，都有对应的 LoRA。

## 原理

全量微调要更新整个模型的权重，又贵又难分发。LoRA 的观察是：微调带来的权重变化往往是「低秩」的——可以用两个小矩阵的乘积 A×B 近似表达。于是冻结原权重、只训练这对小矩阵，训练参数量缩小上万倍，效果却常常不输全量微调。数学细节见[训练与微调](../../01-底层原理/训练与微调.md)。

## 由来与历史

LoRA 论文（arXiv:2106.09685）2021 年发表，原本是为 GPT 这类大语言模型设计的。2022 年底 Stable Diffusion 开源后，社区发现这套方法对图像模型同样好用，配合 kohya-ss 的训练脚本，普通玩家用一张消费级显卡就能训练自己的 LoRA。CivitAI 等平台上的共享 LoRA 很快数以万计。

2023 年起出现「加速 LoRA」这一分支：LCM-LoRA、Turbo-LoRA 把[蒸馏](蒸馏与Turbo.md)的结果打包成 LoRA，挂在原版底模上就能几步出图（A1111 社区为此专门加了 lcm 采样器支持，见 issue #13952）。H3 的 H3-Turbo-Lora 就是这一路线的实例。

## 应用

ComfyUI 里用 **LoraLoader** 节点：串在模型加载器和采样器之间，模型文件放 `models/loras/`，节点上有两个强度参数（`strength_model` 影响画面，`strength_clip` 影响提示词理解），一般先保持相等、在 0.5~1.0 之间调。可以多个 LoraLoader 串联叠加多个 LoRA。

A1111 WebUI 则是在提示词里写 `<lora:文件名:权重>`。无论哪个前端，铁律都一样：**LoRA 必须匹配底模架构**——SD1.5 的 LoRA 装不进 SDXL，SDXL 的装不进 Z-Image，接错了轻则报错重则出鬼图。用 H3-Turbo-Lora 这类加速 LoRA 时还要同步把步数降到个位数、CFG 调低，否则反而过曝。

## 争议 / 讨论

- **LoRA vs 全量微调**：社区共识是 LoRA 学风格够用、学全新概念（新物种、新材质）不如全量微调扎实，但后者成本和分发难度高得多。
- **版权争议**：用画师作品训练的 LoRA 是否侵权，社区与画师群体长期对立，CivitAI 等平台对此的审核政策也反复变动。

## 参见

- [训练与微调](../../01-底层原理/训练与微调.md)
- [蒸馏与Turbo](蒸馏与Turbo.md)
- [风格模型](风格模型.md)
- [Textual Inversion](../加速/TextualInversion.md)
