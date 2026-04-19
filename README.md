# Yuan-agent 🤖

<div align="center">
    <b>一个基于 Python 的多智能体（Multi-Agent）协作框架，实现了多种经典 Agent 设计模式。</b><br><br>
    <img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/OpenAI-API-412991?style=flat-square&logo=openai&logoColor=white" alt="OpenAI">
    <img src="https://img.shields.io/badge/Asyncio-Enabled-green?style=flat-square" alt="Asyncio">
</div>

---

## 📌 项目概览

**Yuan-agent** 是一个多智能体研究与实践框架。项目采用纯异步架构（`asyncio`），通过兼容 OpenAI 格式的接口调用大语言模型（并支持接入 ModelScope 等多提供商）。具备工具调用、并发执行和多 Agent 协作能力。

## ✨ 核心特性

- **多模式支持**：实现了 5 种经典的 Agent 设计模式（纯对话、ReAct、计划-求解、自我反思、任务分流）。
- **完全异步架构**：所有核心逻辑基于 `async/await`，支持工具的并发执行（AsyncExecutor），大幅提升执行效率。
- **安全沙箱工具**：内置基于 AST 解析的安全 `CalculatorTool` 替代原生 `eval`。
- **多模型提供商**：基于 `MyLLM` 方便地切换 OpenAI 官方接口和 ModelScope 接口。
- **依赖精简**：采用 `uv` + `pyproject.toml` 进行包管理。

## 📂 核心模式详解

本框架实现了以下几种 Agent：

1. **SimpleAgent (纯对话)**: 最基础的 Agent，直接完成对话回复。
2. **ReActAgent (推理与行动)**: 经典的 `Thought -> Action -> Observation` 循环。支持工具的**异步并发执行**。
3. **ReflectionAgent (自我反思)**: 采用 `生成 -> 自我批判 -> 修正` 的迭代机制，提升复杂任务的输出质量。
4. **PlanSolveAgent (计划与求解)**: 应对复杂长线任务。先由 LLM 生成步骤计划，再逐步并发调用工具完成。
5. **ManagerAgent (任务路由)**: 充当大脑，分析用户意图后，将子任务路由分发给合适的子 Agent（例如：将搜索任务交给 ReActAgent，将写作任务交给 ReflectionAgent）。

## 🚀 快速开始

### 1. 环境准备与依赖安装

本项目使用现代 Python 包管理工具（兼容 `pip` 和 `uv`）：

```bash
# 安装依赖
pip install -e .
# 或使用 uv
uv sync
```

### 2. 配置环境变量

在项目根目录创建或编辑 `.env` 文件，填入你的模型 API 凭证：

```env
LLM_MODEL_ID=gpt-3.5-turbo
LLM_API_KEY=sk-your-api-key
LLM_BASE_URL=https://api.openai.com/v1
```
*(如果需要使用 ModelScope，可以配置 `MODELSCOPE_API_KEY` 并通过 `MyLLM(provider="modelscope")` 调用)*

### 3. 运行演示代码

**运行并发 ReAct 模式演示：**
```bash
python main.py
```

**运行多智能体协作 (Manager) 演示：**
```bash
python demo_manager.py
```

## 📖 更多文档

详细的系统架构图、文件结构剖析以及底层核心类的使用说明，请参考详细的 [项目全景分析与 Walkthrough](hello_agents/docs/Walkthrough.md)。

## 🛡️ 近期优化

- [x] 修复 `PlanSolveAgent` 同步/异步接口调用异常和 `parse_and_execute_action` 的 bug，现已接入 `AsyncExecutor` 并发执行系统。
- [x] 重构 `CalculatorTool`，弃用不安全的 `eval()`，使用安全严格的 `ast.parse` 构建求值引擎。
- [x] 修复 `MyLLM` 继承时的参数传递异常。
- [x] 统一 `ReActAgent` 与 `PlanSolveAgent` 为全异步并发工作流。
