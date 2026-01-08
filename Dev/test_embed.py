import json
import sys
import requests
import numpy as np

# 计算余弦相似度
def cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)

# API 地址（替换为你的服务地址）
url = "https://embedding.aggpf.gpu-k8s.cloudcore-tu.net/v1/embeddings"

# 测试文本
text_similar_1 = "What is the capital of Japan?"
text_similar_2 = "Which city is the capital of Japan?"
text_different = "The weather is nice today."

payload = {
    "model": "/models/Qwen3-Embedding-8B",  # 模型名称
    "input": [text_similar_1, text_similar_2, text_different]
}

print("Sending request to embedding model...")
try:
    resp = requests.post(url, json=payload, timeout=60)
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    sys.exit(1)

# 检查响应状态
if resp.status_code >= 500:
    print(f"Server error: {resp.status_code}")
    resp.raise_for_status()

data = resp.json()

# 打印完整响应
print("\n--- Full API Response ---")
print(json.dumps(data, indent=2, ensure_ascii=False))

# 提取 embeddings
embedding_list = data.get("data")
if not embedding_list or len(embedding_list) < 3:
    print("Error: Response does not contain expected embeddings.")
    sys.exit(1)

emb_sim_1 = embedding_list[0]["embedding"]
emb_sim_2 = embedding_list[1]["embedding"]
emb_diff = embedding_list[2]["embedding"]

# 打印 embedding 长度
print("\nEmbedding lengths:")
print(f"Sentence 1: {len(emb_sim_1)}")
print(f"Sentence 2: {len(emb_sim_2)}")
print(f"Sentence 3: {len(emb_diff)}")

# 计算相似度
score_similar = cosine_similarity(emb_sim_1, emb_sim_2)
score_different_1 = cosine_similarity(emb_sim_1, emb_diff)

print("\n--- Embedding Model Test Results ---")
print(f"Similarity between similar sentences: {score_similar:.4f}")
print(f"Similarity between different sentences: {score_different_1:.4f}\n")

# 判断测试是否通过
if score_similar > 0.8 and score_different_1 < 0.5:
    print("✅ Test Passed: The model correctly identified similar and different sentences.")
else:
    print("❌ Test Failed: The model may not be working as expected.")