import requests
from openai import OpenAI
import base64
import mimetypes

# 配置
URL = "https://gemma4.aggpf.gpu-k8s.cloudcore-tu.net/v1"
MODEL_NAME = "/models/gemma-4-E4B-it"
client = OpenAI(base_url=URL, api_key="EMPTY")

def test_audio_raw(audio_path):
    """直接用 requests 测试音频 API"""
    
    # 读取音频文件
    print(f"1. 读取音频文件：{audio_path}")
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    print(f"   文件大小：{len(audio_bytes)} bytes")
    
    # 转为 base64
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    audio_format = mimetypes.guess_type(audio_path)[0] or "audio/ogg"
    print(f"   音频格式：{audio_format}")
    print(f"   Base64 长度：{len(audio_b64)} chars")
    
    # 构建请求
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "audio_url",
                        "audio_url": {
                            "url": f"data:{audio_format};base64,{audio_b64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Provide a verbatim, word-for-word transcription of the audio."
                    }
                ]
            }
        ],
        "max_tokens": 1024,
        "temperature": 0.7
    }
    
    print(f"\n2. 发送请求到：{URL}/chat/completions")
    print(f"   模型：{MODEL_NAME}")
    print(f"   Payload 大小：{len(str(payload))} chars")
    
    try:
        resp = requests.post(
            f"{URL}/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=120
        )
        
        print(f"\n3. 响应状态码：{resp.status_code}")
        print(f"   响应头：{dict(resp.headers)}")
        print(f"\n4. 响应内容：")
        print(f"   {resp.text[:2000]}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"\n✅ 成功！转录结果：")
            print(data["choices"][0]["message"]["content"])
        else:
            print(f"\n❌ 错误响应")
            
    except requests.exceptions.Timeout:
        print("\n❌ 请求超时")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求异常：{e}")
    except Exception as e:
        print(f"\n❌ 未知错误：{e}")

def test_audio_model_check():
    """检查服务器模型信息"""
    print("\n" + "="*60)
    print("检查服务器模型信息")
    print("="*60)
    
    try:
        resp = requests.get(
            f"{URL}/v1/models",
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"状态码：{resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"\n服务器可用模型：")
            for model in data.get("data", []):
                model_id = model.get("id", "")
                print(f"  - {model_id}")
                
            # 检查 E4B 模型是否支持音频
            gemma4_models = [m for m in data.get("data", []) if "gemma-4" in m.get("id", "")]
            print(f"\nGemma 4 模型列表：")
            for model in gemma4_models:
                print(f"  - {model.get('id')}")
        else:
            print(f"响应：{resp.text[:500]}")
            
    except Exception as e:
        print(f"检查失败：{e}")

if __name__ == "__main__":
    # 检查服务器模型
    test_audio_model_check()
    
    # 测试音频转录
    print("\n" + "="*60)
    print("测试音频转录")
    print("="*60)
    test_audio_raw("こんにちは.ogg")
