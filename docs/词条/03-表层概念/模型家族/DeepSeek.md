---
term: DeepSeek 系列
full_name: DeepSeek (深度求索模型家族)
aliases: [DeepSeek V3, DeepSeek V4, DeepSeek R1]
category: 模型
dimension: 模型家族
granularity: 家族
maturity: stable
status: draft
contributors: [TEXXXXTURE]
sources:
  - https://huggingface.co/deepseek-ai
  - https://arxiv.org/abs/2405.04434
relations:
  - target: DeepSeek
    note: 厂商词条
  - target: Qwen
    note: DeepSeek 和 Qwen 是中文开源 LLM 的主要竞争者
  - target: MoE
    note: DeepSeek V2+ 采用 MoE 架构
created: 2026-08-17
updated: 2026-08-17
revisions: 1
---

## 定义

DeepSeek 是深度求索的大语言模型家族,以 MoE(混合专家)架构和极致性价比闻名。从 V2 开始引入 MLA(多头潜在注意力)+DeepSeekMoE 架构,用更少的激活参数实现更强能力。最新 DeepSeek V4 Pro 智能指数 53.2,价格仅 $1.32/$3.96——同档位最便宜。

## 由来与历史

DeepSeek V2(2024.05)首发 MoE+MLA 架构,236B 总参数/21B 激活,价格战一炮打响。DeepSeek V3(2025.01)进一步优化训练效率。DeepSeek R1(2025.01)是开源推理模型标杆。DeepSeek V4 Pro(2026)是当前版本,价格持续下探。

## 应用

DeepSeek V4 Pro 在 AA 评测中:智能指数 53.2,输出速度 80 tok/s,输入 $1.32/M、输出 $3.96/M、缓存命中 $0.044/M。同档位(50+ 分)里价格最低。通过 deepseek.com 或第三方 API(硅基流动、OpenRouter)调用。本地部署需大显存(66GB+),推荐 GGUF 量化版。

## AA 评测数据 (2026-08-17)

- 智能指数: 53.2
- 输出速度: 80.22 tok/s
- 输入价格: $1.32/M tokens
- 输出价格: $3.96/M tokens
- 缓存命中: $0.044/M tokens
- 上下文窗口: 1M
- 全知指数: 0.83

## 参见

- [模型数据总览](../../04-LLM工程/模型数据总览.md)
- [模型评测](../../04-LLM工程/模型评测.md)
