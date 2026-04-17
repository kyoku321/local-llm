import json
import time
import requests
from openai import OpenAI
from pathlib import Path

# 定义 API 配置
URL = "https://aggpf-qwen35-35b.gpu-k8s.cloudcore-tu.net/v1"
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

def process_article_with_qwen(title, link, enable_thinking=False):
    """
    使用 Qwen 模型直接打印返回内容，不进行结构化解析。
    
    Args:
        title: 文章标题
        link: 文章链接
        enable_thinking: 是否启用 thinking 参数（默认为 False）
    
    Returns:
        tuple: (模型返回内容，请求耗时)
    """
    article_text = get_article_text(link)
    if not article_text:
        return "記事のコンテンツを取得できませんでした。", 0

    prompt = f"""
    あなたは優秀な編集者です。以下のタスクを実行してください。

    1. 記事のタイトルを自然な日本語に翻訳してください。元のタイトルが日本語の場合は、そのままで構いません。
    2. 記事の本文を日本語で 200 字以内に要約してください。
    3. 記事の内容に最も関連性の高いキーワードタグを三つ以内に抽出してください。

    記事タイトル："{title}"
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
        start_time = time.time()
        
        # 构建 extra_body 参数
        extra_body = {
            "top_k": 20,
            "chat_template_kwargs": {
                "enable_thinking": enable_thinking
            }
        }
        
        chat_response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=32768,
            temperature=0.7,
            top_p=0.8,
            presence_penalty=1.5,
            extra_body=extra_body
        )
        
        total_time = time.time() - start_time
        return chat_response.choices[0].message.content, total_time
    except Exception as e:
        return f"Request Error: {str(e)}", 0

if __name__ == "__main__":
    test_title = "特朗普赢得大选"
    test_link = "https://www.ibm.com/cn-zh/think/topics/agent2agent-protocol"
    
    print(f"=" * 60)
    print(f"Testing Qwen3.5-35B-A3B - Thinking Parameter Impact")
    print(f"=" * 60)
    print(f"Test Article: {test_title}")
    print(f"Test Link: {test_link}")
    print()
    
    # 抑制 SSL 警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # 测试 1: 关闭 thinking
    print("-" * 60)
    print("[TEST 1] enable_thinking=False")
    print("-" * 60)
    
    start_test1 = time.time()
    content1, total_time1 = process_article_with_qwen(
        test_title, test_link, enable_thinking=False
    )
    end_test1 = time.time()
    
    print(f"✓ 请求总耗时：{total_time1:.2f} 秒")
    print(f"✓ 模型返回内容:\n{content1}")
    
    # 测试 2: 开启 thinking
    print()
    print("-" * 60)
    print("[TEST 2] enable_thinking=True")
    print("-" * 60)
    
    start_test2 = time.time()
    content2, total_time2 = process_article_with_qwen(
        test_title, test_link, enable_thinking=True
    )
    end_test2 = time.time()
    
    print(f"✓ 请求总耗时：{total_time2:.2f} 秒")
    print(f"✓ 模型返回内容:\n{content2}")
    
    # 对比结果
    print()
    print("=" * 60)
    print("[PERFORMANCE COMPARISON]")
    print("=" * 60)
    time_diff = total_time2 - total_time1
    
    print(f"关闭 thinking 耗时：{total_time1:.2f} 秒")
    print(f"开启 thinking 耗时：{total_time2:.2f} 秒")
    print(f"时间差：{abs(time_diff):.2f} 秒")
    print(f"思考额外耗时：{time_diff:.2f} 秒") if time_diff > 0 else print(f"节省时间：{abs(time_diff):.2f} 秒")
