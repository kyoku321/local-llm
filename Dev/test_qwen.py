import json
import time
import requests
from openai import OpenAI
from pathlib import Path

# 定义 API 配置
URL = "https://qwen35b.aggpf.gpu-k8s.cloudcore-tu.net/v1"
MODEL_NAME = "/models/Qwen3.5-35B-A3B"

client = OpenAI(
    base_url=URL,
    api_key="EMPTY"
)

def get_article_text(link):
    """
    简单的文章抓取函数。
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        resp = requests.get(link, headers=headers, timeout=15)
        resp.raise_for_status()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        print(f"Error fetching article text: {e}")
        return None

def process_article_with_qwen(title, link):
    """
    使用 Qwen 模型直接打印返回内容，不进行结构化解析。
    """
    article_text = get_article_text(link)
    if not article_text:
        return "記事のコンテンツを取得できませんでした。"

    prompt = f"""
    あなたは優秀な編集者です。以下のタスクを実行してください。

    1. 記事のタイトルを自然な日本語に翻訳してください。元のタイトルが日本語の場合は、そのままで構いません。
    2. 記事の本文を日本語で200字以内に要約してください。
    3. 記事の内容に最も関連性の高いキーワードタグを三つ以内に抽出してください。

    記事タイトル: "{title}"
    記事本文:
    ---
    {article_text[:5000]}
    ---
    """

    messages = [
        {"role": "system", "content": "你是一个专业的编辑和翻译助手。"},
        {"role": "user", "content": prompt}
    ]

    try:
        chat_response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=0.95,
            presence_penalty=1.5,
            extra_body={
                "top_k": 20,
            }
        )
        return chat_response.choices[0].message.content
    except Exception as e:
        return f"Request Error: {str(e)}"

if __name__ == "__main__":
    test_title = "特朗普赢得大选"
    test_link = "https://www.ibm.com/cn-zh/think/topics/agent2agent-protocol"
    
    print(f"--- 正在使用 Qwen3-235B 测试原始输出 ---")
    print(f"原始标题: {test_title}")
    
    # 抑制 SSL 警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    content = process_article_with_qwen(test_title, test_link)
    
    print(f"\n[模型返回内容]:\n{content}")
