# AI 知识地图

> 这不是一张目录表，而是一张**网状入口**：词条是节点，关系是边。本页由 `docs/词条/` 的 frontmatter 自动汇总生成，与词条实时同步（新增/修改词条后重跑生成脚本即可）。

> 图例：[稳定] 已沉淀（stable） · [热词] 社区热词（hot） · 🆕 本批新增（2026-08-17）

## 一、底层原理（根：原理层）

- [稳定] [DiT](../词条/01-底层原理/DiT.md) · 架构 🆕
- [热词] [MoE](../词条/01-底层原理/MoE.md) · 架构
- [稳定] [Transformer](../词条/01-底层原理/Transformer.md) · 架构
- [稳定] [强化学习](../词条/01-底层原理/强化学习.md) · 训练 🆕
- [稳定] [扩散模型](../词条/01-底层原理/扩散模型.md) · 多模态
- [稳定] [注意力机制](../词条/01-底层原理/注意力机制.md) · 架构
- [稳定] [浮点数与精度](../词条/01-底层原理/浮点数与精度.md) · 架构
- [稳定] [生成模型](../词条/01-底层原理/生成模型.md) · 架构
- [稳定] [神经网络](../词条/01-底层原理/神经网络.md) · 架构
- [稳定] [缩放法则](../词条/01-底层原理/缩放法则.md) · 架构 🆕
- [稳定] [训练与微调](../词条/01-底层原理/训练与微调.md) · 训练
- [稳定] [量化](../词条/01-底层原理/量化.md) · 推理

## 二、组件（枝：模型零件）

- [稳定] [CLIP](../词条/02-组件/CLIP.md) · 多模态
- [稳定] [Tokenizer](../词条/02-组件/Tokenizer.md) · 架构
- [稳定] [UNet](../词条/02-组件/UNet.md) · 架构
- [稳定] [VAE](../词条/02-组件/VAE.md) · 多模态
- [热词] [嵌入层](../词条/02-组件/嵌入层.md) · 架构
- [稳定] [文本编码器](../词条/02-组件/文本编码器.md) · 多模态
- [稳定] [潜空间](../词条/02-组件/潜空间.md) · 多模态
- [稳定] [采样器](../词条/02-组件/采样器.md) · 推理

## 三、表层概念（叶：具体技术/格式/参数）

### 量化格式

- [稳定] [GGUF](../词条/03-表层概念/量化格式/GGUF.md) · 推理
- [稳定] [bf16](../词条/03-表层概念/量化格式/bf16.md) · 推理
- [稳定] [int8与fp8量化](../词条/03-表层概念/量化格式/int8与fp8量化.md) · 推理
- [稳定] [safetensors](../词条/03-表层概念/量化格式/safetensors.md) · 推理

### 微调

- [稳定] [LoRA](../词条/03-表层概念/微调/LoRA.md) · 模型微调
- [稳定] [PEFT](../词条/03-表层概念/微调/PEFT.md) · 模型微调 🆕
- [稳定] [全量微调](../词条/03-表层概念/微调/全量微调.md) · 模型微调 🆕
- [稳定] [蒸馏与Turbo](../词条/03-表层概念/微调/蒸馏与Turbo.md) · 训练
- [稳定] [风格模型](../词条/03-表层概念/微调/风格模型.md) · 模型微调

### 加速

- [热词] [IP-Adapter](../词条/03-表层概念/加速/IP-Adapter.md) · 多模态
- [稳定] [SageAttention](../词条/03-表层概念/加速/SageAttention.md) · 推理
- [稳定] [Textual Inversion](../词条/03-表层概念/加速/TextualInversion.md) · 模型微调

### 对齐

- [稳定] [DPO](../词条/03-表层概念/对齐/DPO.md) · 对齐
- [稳定] [RLHF](../词条/03-表层概念/对齐/RLHF.md) · 对齐
- [稳定] [对齐](../词条/03-表层概念/对齐/对齐.md) · 对齐 🆕
- [稳定] [提示注入](../词条/03-表层概念/对齐/提示注入.md) · 对齐 🆕
- [稳定] [越狱](../词条/03-表层概念/对齐/越狱.md) · 对齐

### 模型厂商

- [稳定] [Black Forest Labs](../词条/03-表层概念/模型厂商/Black Forest Labs.md) · 平台
- [稳定] [Lightricks](../词条/03-表层概念/模型厂商/Lightricks.md) · 平台
- [稳定] [Meta](../词条/03-表层概念/模型厂商/Meta.md) · 平台
- [稳定] [MiniMax](../词条/03-表层概念/模型厂商/MiniMax.md) · 平台
- [稳定] [Stability AI](../词条/03-表层概念/模型厂商/Stability AI.md) · 平台
- [稳定] [阿里](../词条/03-表层概念/模型厂商/阿里.md) · 平台

### 模型家族

- [热词] [ACE-Step](../词条/03-表层概念/模型家族/ACE-Step.md) · 模型
- [稳定] [FLUX](../词条/03-表层概念/模型家族/FLUX.md) · 模型
- [稳定] [LTX](../词条/03-表层概念/模型家族/LTX.md) · 模型
- [稳定] [Llama](../词条/03-表层概念/模型家族/Llama.md) · 模型
- [稳定] [MiniMax H3](../词条/03-表层概念/模型家族/MiniMax H3.md) · 模型
- [稳定] [MusicGen](../词条/03-表层概念/模型家族/MusicGen.md) · 模型
- [稳定] [Qwen](../词条/03-表层概念/模型家族/Qwen.md) · 模型
- [热词] [Stable Audio](../词条/03-表层概念/模型家族/Stable Audio.md) · 模型
- [稳定] [Stable Diffusion](../词条/03-表层概念/模型家族/Stable Diffusion.md) · 模型
- [稳定] [Wan](../词条/03-表层概念/模型家族/Wan.md) · 模型
- [稳定] [Z-Image](../词条/03-表层概念/模型家族/Z-Image.md) · 模型

### 工具

- [热词] [CivitAI](../词条/03-表层概念/工具/CivitAI.md) · 平台
- [稳定] [ComfyUI](../词条/03-表层概念/工具/ComfyUI.md) · 工具
- [热词] [Hugging Face](../词条/03-表层概念/工具/Hugging Face.md) · 平台
- [稳定] [KS](../词条/03-表层概念/工具/KS.md) · 工具
- [稳定] [KSampler](../词条/03-表层概念/工具/KSampler.md) · 工具
- [稳定] [Ollama](../词条/03-表层概念/工具/Ollama.md) · 工具

### 多模态

- [稳定] [ControlNet](../词条/03-表层概念/多模态/ControlNet.md) · 多模态 🆕

### LLM

- [稳定] [KV Cache](../词条/03-表层概念/LLM/KV Cache.md) · 推理
- [稳定] [RAG](../词条/03-表层概念/LLM/RAG.md) · 上下文工程
- [稳定] [上下文窗口](../词条/03-表层概念/LLM/上下文窗口.md) · 上下文工程

### Agent

- [稳定] [Agent](../词条/03-表层概念/Agent/Agent.md) · Agent
- [稳定] [Function Calling](../词条/03-表层概念/Agent/Function Calling.md) · Agent
- [热词] [MCP](../词条/03-表层概念/Agent/MCP.md) · Agent

## 四、LLM 工程（落地层）

- [热词] [PagedAttention](../词条/04-LLM工程/PagedAttention.md) · 推理
- [热词] [RAG 工程](../词条/04-LLM工程/RAG 工程.md) · 上下文工程
- [热词] [微调工程](../词条/04-LLM工程/微调工程.md) · 训练
- [热词] [投机解码](../词条/04-LLM工程/投机解码.md) · 推理
- [稳定] [推理优化](../词条/04-LLM工程/推理优化.md) · 推理 🆕
- [热词] [推理引擎](../词条/04-LLM工程/推理引擎.md) · 推理
- [热词] [提示词工程](../词条/04-LLM工程/提示词工程.md) · 上下文工程
- [热词] [模型数据总览](../词条/04-LLM工程/模型数据总览.md) · 推理 🆕
- [热词] [模型评测](../词条/04-LLM工程/模型评测.md) · 训练

## 五、Agent 工程（智能体开发）

- [热词] [Agent 框架](../词条/05-Agent工程/Agent 框架.md) · Agent
- [热词] [ReAct](../词条/05-Agent工程/ReAct.md) · Agent
- [热词] [多 Agent 协作](../词条/05-Agent工程/多 Agent 协作.md) · Agent
- [热词] [工作流编排](../词条/05-Agent工程/工作流编排.md) · Agent
- [热词] [工具调用](../词条/05-Agent工程/工具调用.md) · Agent
- [热词] [记忆系统](../词条/05-Agent工程/记忆系统.md) · Agent

## 六、计算机基础（IT 行业）

### 框架与库

- [稳定] [AntDesign](../词条/06-IT行业/框架与库/AntDesign.md) · 工具 🆕
- [热词] [Astro](../词条/06-IT行业/框架与库/Astro.md) · 工具 🆕
- [稳定] [Diffusers库](../词条/06-IT行业/框架与库/Diffusers库.md) · 工具
- [热词] [Electron](../词条/06-IT行业/框架与库/Electron.md) · 工具
- [稳定] [FastAPI](../词条/06-IT行业/框架与库/FastAPI.md) · 工具
- [热词] [Gradio](../词条/06-IT行业/框架与库/Gradio.md) · 工具
- [稳定] [JAX](../词条/06-IT行业/框架与库/JAX.md) · 工具
- [热词] [LangChain](../词条/06-IT行业/框架与库/LangChain.md) · 工具
- [稳定] [LlamaIndex](../词条/06-IT行业/框架与库/LlamaIndex.md) · 工具
- [热词] [NaiveUI](../词条/06-IT行业/框架与库/NaiveUI.md) · 工具 🆕
- [热词] [Next.js](../词条/06-IT行业/框架与库/Next.js.md) · 工具
- [稳定] [Node.js](../词条/06-IT行业/框架与库/Node.js.md) · 工具
- [稳定] [NumPy](../词条/06-IT行业/框架与库/NumPy.md) · 工具
- [稳定] [ONNX](../词条/06-IT行业/框架与库/ONNX.md) · 工具
- [稳定] [Pandas](../词条/06-IT行业/框架与库/Pandas.md) · 工具
- [稳定] [PyTorch](../词条/06-IT行业/框架与库/PyTorch.md) · 工具
- [热词] [React](../词条/06-IT行业/框架与库/React.md) · 工具
- [热词] [Streamlit](../词条/06-IT行业/框架与库/Streamlit.md) · 工具
- [稳定] [Tailwind](../词条/06-IT行业/框架与库/Tailwind.md) · 工具 🆕
- [热词] [Tauri](../词条/06-IT行业/框架与库/Tauri.md) · 工具 🆕
- [稳定] [TensorFlow](../词条/06-IT行业/框架与库/TensorFlow.md) · 工具
- [稳定] [Transformers库](../词条/06-IT行业/框架与库/Transformers库.md) · 工具
- [稳定] [Vite](../词条/06-IT行业/框架与库/Vite.md) · 工具 🆕
- [热词] [Vue](../词条/06-IT行业/框架与库/Vue.md) · 工具
- [热词] [Wails](../词条/06-IT行业/框架与库/Wails.md) · 工具 🆕
- [热词] [shadcn](../词条/06-IT行业/框架与库/shadcn.md) · 工具 🆕
- [稳定] [llama.cpp](../词条/06-IT行业/框架与库/llama.cpp.md) · 工具
- [热词] [vLLM](../词条/06-IT行业/框架与库/vLLM.md) · 推理


## 本批新增（🆕 2026-08-17）

补齐了此前被引用却尚无页面的概念，并织密关系网：

- [ControlNet](../词条/03-表层概念/多模态/ControlNet.md) — ControlNet
- [DiT](../词条/01-底层原理/DiT.md) — Diffusion Transformer
- [PEFT](../词条/03-表层概念/微调/PEFT.md) — Parameter-Efficient Fine-Tuning
- [全量微调](../词条/03-表层概念/微调/全量微调.md) — Full Fine-tuning
- [对齐](../词条/03-表层概念/对齐/对齐.md) — AI Alignment
- [强化学习](../词条/01-底层原理/强化学习.md) — Reinforcement Learning
- [推理优化](../词条/04-LLM工程/推理优化.md) — Inference Optimization
- [提示注入](../词条/03-表层概念/对齐/提示注入.md) — Prompt Injection
- [模型数据总览](../词条/04-LLM工程/模型数据总览.md) — AI Model Data Overview
- [缩放法则](../词条/01-底层原理/缩放法则.md) — Scaling Law

## 规划方向（待补，供下一轮）

基于现有关系网与 AIGC/LLM/Agent 主线，建议下一轮优先补：

- **方法论补强**：反向传播、激活函数、CNN/RNN、嵌入与向量、多模态（概念页）
- **工程闭环**：MLOps / LLMOps、模型服务与部署、分布式训练、数据工程
- **安全伦理**：提示注入已建，可补 偏见/隐私/AI 治理/版权与许可协议
- **生态补齐**：更多模型厂商与模型家族（如 SD3、Hunyuan、Sora 类视频模型）
- **ComfyUI 工作流专题**：节点、KSampler、Loaders 系列实操词条

> 想加词条？直接按 `docs/词条/` 下对应目录新建 `.md`，填好 frontmatter 的 `relations`（target 必须指向已存在词条或本批待建清单）即可 —— 导航树与首页栏目会自动长出来，不需要手工登记。提交前跑一遍 `python scripts/validate_content.py`。

## 本批新增（🆕 2026-08-23 · 前端框架）

基于 TabTin 产品拆解（07-拆解报告），补充"AI 时代前端标准配方"相关的框架与库词条，织入已有 React/Vue/Electron/Next.js 关系网：

- [Tailwind](../词条/06-IT行业/框架与库/Tailwind.md) — 原子化 CSS，AI 生成前端的事实标准
- [shadcn](../词条/06-IT行业/框架与库/shadcn.md) — 复制粘贴式组件库，AI SaaS 三件套之一
- [Vite](../词条/06-IT行业/框架与库/Vite.md) — 前端构建工具事实标准（electron-vite）
- [Tauri](../词条/06-IT行业/框架与库/Tauri.md) — Electron 的轻量替代（Rust 后端）
- [Wails](../词条/06-IT行业/框架与库/Wails.md) — 轻量桌面框架（Go 后端）
- [AntDesign](../词条/06-IT行业/框架与库/AntDesign.md) — React 企业级组件库
- [NaiveUI](../词条/06-IT行业/框架与库/NaiveUI.md) — Vue 3 组件库
- [Astro](../词条/06-IT行业/框架与库/Astro.md) — 内容站/文档站框架
