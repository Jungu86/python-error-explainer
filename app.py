import json
import httpx
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:1.5b"

SYSTEM_PROMPT = """你是一个 Python 报错解释器。
用户会粘贴 Python 报错信息或代码。
请按下面格式回答：
1. 错误原因
2. 出错位置
3. 怎么修复
4. 修复后的代码
如果信息不足，先问一个最关键的澄清问题。"""


class AskRequest(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
async def index():
    return Path("templates/index.html").read_text(encoding="utf-8")


# 保留原来的非流式接口作为备用
@app.post("/api/ask")
async def ask(req: AskRequest):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.question},
        ],
        "stream": False,
        "options": {"temperature": 0.2}
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(OLLAMA_URL, json=payload)
        resp.raise_for_status()
        data = resp.json()
    return {"answer": data["message"]["content"]}


# 新增：流式输出接口
@app.post("/api/chat/stream")
async def chat_stream(req: AskRequest):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.question},
        ],
        "stream": True,  # 开启 Ollama 流式模式
        "options": {"temperature": 0.2}
    }

    async def generate():
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("POST", OLLAMA_URL, json=payload) as response:
                async for chunk in response.aiter_lines():
                    if chunk:
                        data = json.loads(chunk)
                        if "message" in data and "content" in data["message"]:
                            # 包装成 SSE 格式（Server-Sent Events）
                            content = data["message"]["content"]
                            yield f"data: {json.dumps({'content': content})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
