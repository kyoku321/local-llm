import json
import sys
import time
import requests
import yaml
from pathlib import Path

# 定义 API 配置
# 注意：这里使用 HTTPS，前提是您的 Ingress TLS 证书已正确配置
URL = "https://qwen.aggpf.gpu-k8s.cloudcore-tu.net/v1/chat/completions"
MODEL_NAME = "/models/Qwen3-235B-A22B-Instruct-2507-FP8"

def get_article_text(link):
    """
    简单的文章抓取函数。实际生产环境建议使用 trafilatura 或 BeautifulSoup。
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        resp = requests.get(link, headers=headers, timeout=15)
        resp.raise_for_status()
        # 这里做一个极简的处理：如果是 HTML，只取一部分文本。
        # 在实际测试中，如果用户环境没装 BeautifulSoup，可以先用这个占位。
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, 'html.parser')
        # 移除脚本和样式
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        print(f"Error fetching article text: {e}")
        return None

def process_article_with_qwen(title, link):
    """
    使用 Qwen 模型生成翻译后的标题、摘要和标签。
    融合了商用环境的 Prompt 逻辑。
    """
    article_text = get_article_text(link)
    if not article_text:
        return title, "記事のコンテンツを取得できませんでした。", []

    # 商用环境 Prompt
    prompt = f"""
    あなたは優秀な編集者です。以下のタスクを実行してください。

    1. 記事のタイトルを自然な日本語に翻訳してください。元のタイトルが日本語の場合は、そのままで構いません。
    2. 記事の本文を日本語で200字以内に要約してください。
    3. 記事の内容に最も関連性の高いキーワードタグを三つ以内に抽出してください。(考えられるタグ例: "AI", "eSIM", "5G", "Operator"等)

    記事タイトル: "{title}"
    記事本文:
    ---
    {article_text[:15000]}
    ---

    レスポンスは以下のJSON形式で、翻訳されたタイトルと要約のみを返してください。
    {{
      "translated_title": "ここに翻訳したタイトル",
      "summary": "ここに要約",
      "labels": ["tag1", "tag2", "tag3"]
    }}
    """

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "你是一个专业的编辑和翻译助手，严格按照 JSON 格式输出结果。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2048,
        "temperature": 0.3, # 降低温度以获得更稳定的 JSON 输出
        # "response_format": {"type": "json_object"} # 如果 vLLM 版本支持，建议开启
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 忽略证书验证 (verify=False) 以防自签名证书报错，生产环境建议开启
            resp = requests.post(URL, json=payload, timeout=120, verify=False)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            
            # 清理 Markdown 代码块包裹（常见问题）
            cleaned_text = content.replace("```json", "").replace("```", "").strip()
            
            # 使用 yaml 解析（如请求中所述）或 json
            result = yaml.safe_load(cleaned_text)
            
            translated_title = result.get("translated_title", title)
            summary = result.get("summary", "要約を生成できませんでした。")
            labels = result.get("labels", [])
            
            return translated_title, summary, labels
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                return title, f"AIによる要約中にエラーが発生しました: {str(e)}", []

if __name__ == "__main__":
    # 使用相同的测试文章
    test_title = "特朗普赢得大选"
    test_link = "https://www.ibm.com/cn-zh/think/topics/agent2agent-protocol"
    
    print(f"--- 正在使用 Qwen3-235B 测试商用 Prompt ---")
    print(f"原始标题: {test_title}")
    
    # 抑制 urllib3 的 InsecureRequestWarning 警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    t_title, summary, labels = process_article_with_qwen(test_title, test_link)
    
    print(f"\n[翻译标题]: {t_title}")
    print(f"[内容摘要]: {summary}")
    print(f"[标签]: {', '.join(labels)}")
