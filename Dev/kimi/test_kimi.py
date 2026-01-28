import json
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://kimi.aggpf.gpu-k8s.cloudcore-tu.net/v1/chat/completions"
MODEL_NAME = "moonshotai/Kimi-K2.5"

def send_test_prompt(prompt, enable_thinking=True, temperature=None, top_p=0.95, max_tokens=4096):
    """
    发送测试提示词，观察 Thinking 模式的输出。

    Args:
        prompt: 用户输入的提示词
        enable_thinking: 是否启用 Thinking 模式
        temperature: 温度参数（Thinking 模式默认 1.0，Instant 模式默认 0.6）
        top_p: Top-p 采样参数（推荐 0.95）
        max_tokens: 最大生成 token 数

    Returns:
        响应内容或 None（如果出错）
    """
    if temperature is None:
        temperature = 1.0 if enable_thinking else 0.6

    print(f"\n{'='*50}")
    print(f"[Test Config] Thinking: {enable_thinking} | Temp: {temperature} | Top-p: {top_p}")
    print(f"[Prompt]: {prompt}")
    print(f"{'='*50}\n")

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
    }

    if enable_thinking:
        payload["extra_body"] = {"chat_template_kwargs": {"thinking": True}}
    else:
        payload["extra_body"] = {"chat_template_kwargs": {"thinking": False}}

    try:
        start_time = time.time()
        resp = requests.post(URL, json=payload, timeout=300, verify=False)
        resp.raise_for_status()
        end_time = time.time()

        data = resp.json()
        message = data["choices"][0]["message"]
        content = message.get("content", "")
        reasoning_content = message.get("reasoning_content", "")

        print(f"--- Response (Time: {end_time - start_time:.2f}s) ---")

        if reasoning_content:
            print(f"[Reasoning Content]:")
            print(reasoning_content)
            print("\n[Final Answer]:")

        print(content)
        print("-" * 50)

        return content
    except Exception as e:
        print(f"Error executing request: {e}")
        return None

def send_multimodal_test(image_url, prompt, enable_thinking=True, temperature=None):
    """
    发送多模态测试（图像输入）。

    Args:
        image_url: 图像 URL（支持 base64 编码的 data URL）
        prompt: 文本提示词
        enable_thinking: 是否启用 Thinking 模式
        temperature: 温度参数

    Returns:
        响应内容或 None
    """
    if temperature is None:
        temperature = 1.0 if enable_thinking else 0.6

    print(f"\n{'='*50}")
    print(f"[Multimodal Test] Thinking: {enable_thinking} | Image URL: {image_url}")
    print(f"[Prompt]: {prompt}")
    print(f"{'='*50}\n")

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
        "max_tokens": 4096,
        "temperature": temperature,
        "top_p": 0.95,
    }

    if enable_thinking:
        payload["extra_body"] = {"chat_template_kwargs": {"thinking": True}}
    else:
        payload["extra_body"] = {"chat_template_kwargs": {"thinking": False}}

    try:
        start_time = time.time()
        resp = requests.post(URL, json=payload, timeout=300, verify=False)
        resp.raise_for_status()
        end_time = time.time()

        data = resp.json()
        message = data["choices"][0]["message"]
        content = message.get("content", "")
        reasoning_content = message.get("reasoning_content", "")

        print(f"--- Response (Time: {end_time - start_time:.2f}s) ---")

        if reasoning_content:
            print(f"[Reasoning Content]:")
            print(reasoning_content)
            print("\n[Final Answer]:")

        print(content)
        print("-" * 50)

        return content
    except Exception as e:
        print(f"Error executing multimodal request: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("Kimi-K2.5 Testing Suite")
    print("=" * 60)

    prompt_logic = "9.11 和 9.9 哪个数值更大？请详细解释你的比较过程。"
    print("\n>>> 测试用例 1：逻辑陷阱题（Thinking 模式）")
    send_test_prompt(prompt_logic, enable_thinking=True)

    print("\n>>> 测试用例 4：对比测试 - 关闭 Thinking 模式")
    send_test_prompt(prompt_logic, enable_thinking=False)

    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)