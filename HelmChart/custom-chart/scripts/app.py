from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from vllm import LLM
import os

# 模型路径
MODEL_PATH = os.environ["MODEL_PATH"]

# 初始化 vLLM 模型（embedding 模式）
llm = LLM(model=MODEL_PATH, task="embed")

# 创建 FastAPI 应用
app = FastAPI()

# 请求体定义
class EmbeddingRequest(BaseModel):
    model: str
    input: List[str]

# 响应体定义
class EmbeddingData(BaseModel):
    object: str = "embedding"
    embedding: List[float]
    index: int

class EmbeddingResponse(BaseModel):
    object: str = "list"
    data: List[EmbeddingData]
    model: str

@app.post("/v1/embeddings", response_model=EmbeddingResponse)
async def create_embeddings(req: EmbeddingRequest):
    # 调用 vLLM 生成 embeddings
    outputs = llm.embed(req.input)
    embeddings = [o.outputs.embedding for o in outputs]

    # 构造响应
    data = [
        EmbeddingData(embedding=embeddings[i], index=i)
        for i in range(len(embeddings))
    ]
    return EmbeddingResponse(data=data, model=req.model)

@app.get("/health")
async def health_check():
    return {"status": "ok"}