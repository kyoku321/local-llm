import json
import requests
import urllib3

# 禁用证书警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API 配置
URL = "https://glm.aggpf.gpu-k8s.cloudcore-tu.net/v1/chat/completions"
MODEL_NAME = "glm-4.7-fp8"

def send_test_prompt(prompt, enable_thinking=True, temperature=0.7, top_p=1.0, max_new_tokens=4096):
    """
    发送测试提示词，观察 Thinking 模式的输出。
    """
    print(f"\n{'='*50}")
    print(f"[Test Config] Thinking: {enable_thinking} | Temp: {temperature}")
    print(f"[Prompt]: {prompt}")
    print(f"{'='*50}\n")

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_new_tokens,
        "temperature": temperature,
        "top_p": top_p,
    }

    # 控制 Thinking 模式
    if enable_thinking:
        payload["extra_body"] = {"chat_template_kwargs": {"enable_thinking": True}}
    else:
        payload["extra_body"] = {"chat_template_kwargs": {"enable_thinking": False}}

    try:
        start_time = time.time()
        # verify=False 用于绕过自签名证书验证
        resp = requests.post(URL, json=payload, timeout=300, verify=False)
        resp.raise_for_status()
        end_time = time.time()
        
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        
        print(f"--- Response (Time: {end_time - start_time:.2f}s) ---")
        print(content)
        print("-" * 50)
        
        return content
    except Exception as e:
        print(f"Error executing request: {e}")
        return None

import time

if __name__ == "__main__":
    # 测试用例 1: 经典的逻辑陷阱题 (Thinking ON)
    # 这类题目通常需要模型“停下来想一想”才能避免直接回答常见的错误答案
    prompt_logic = "9.11 和 9.9 哪个数值更大？请详细解释你的比较过程。"
    # send_test_prompt(prompt_logic, enable_thinking=True)

    # 测试用例 2: 复杂逻辑谜题 (Thinking ON)
    # prompt_riddle = "这里有三个盒子，一个装满苹果，一个装满橘子，还有一个装满苹果和橘子。三个盒子的标签都贴错了。你只能打开其中一个盒子，拿出一个水果看一眼，然后你需要纠正所有盒子的标签。请描述你的逻辑步骤。"
    # send_test_prompt(prompt_riddle, enable_thinking=True)

    # 测试用例 3: 对比测试 - 关闭 Thinking (Thinking OFF)
    # 用同样的问题对比回答质量
    print("\n>>> 对比测试：关闭 Thinking 模式")
    send_test_prompt(prompt_logic, enable_thinking=False)
