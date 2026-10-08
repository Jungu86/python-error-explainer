# 🐍 CodeExplainer (Python 报错解释器)

基于 Ollama + FastAPI 的本地化 Python 报错解释助手。支持在本地低资源环境下运行大模型，为 Python 初学者提供报错解析、修复建议与代码示例。

## ✨ 功能特性
- 本地部署大模型（Qwen2.5-1.5B），无需付费 API，数据隐私安全
- 前后端完整闭环，支持网页端直接交互
- **流式输出**（像 ChatGPT 一样打字机效果）
- 提供 REST API 接口，方便二次开发
- 针对低资源环境（16G 内存）进行适配

## 📸 演示截图
![项目演示](demo.png)

## 🛠️ 技术栈
- 后端：Python / FastAPI / httpx
- 大模型：Ollama / Qwen2.5-1.5B
- 前端：原生 HTML / CSS / JavaScript (SSE 流式接收)

## 🚀 快速开始
1. 安装并启动 Ollama，拉取模型：
   ```bash
   ollama pull qwen2.5:1.5b

2 .安装依赖
pip install -r requirements.txt

3. 启动服务
uvicorn app:app --reload

4. 浏览器访问
uvicorn app:app --reload


