import requests
from openai import OpenAI
import base64
import urllib3
import mimetypes
import time

# 配置
URL = "https://gemma4.aggpf.gpu-k8s.cloudcore-tu.net/v1"
# 注意：音频功能只能在 Gemma 4 E2B 或 E4B 模型上运行
# MODEL_NAME = "/models/gemma-4-31B-it"  # 当前模型不支持音频
# MODEL_NAME = "/models/gemma-4-E2B-it"  # 支持音频的模型（如果可用）
MODEL_NAME = "/models/gemma-4-E4B-it"  # 当前使用的模型
client = OpenAI(base_url=URL, api_key="EMPTY")


def test_text_generation():
    """测试文本生成"""
    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Write a poem about the ocean."}],
            max_tokens=512,
            temperature=0.7
        )
        print(resp.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")


def test_single_image(image_url):
    """测试单图理解 - 支持远程 URL 或本地文件"""
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # 获取图片数据
        if image_url.startswith("http"):
            print(f"Downloading: {image_url}")
            headers = {"User-Agent": "Chrome/120.0.0.0 Safari/537.36"}
            resp = requests.get(image_url, headers=headers, verify=False, timeout=30)
            resp.raise_for_status()
            img_bytes = resp.content
        else:
            print(f"Loading local file: {image_url}")
            with open(image_url, "rb") as f:
                img_bytes = f.read()
        
        img_format = mimetypes.guess_type(image_url)[0] or "jpeg"
        img_b64 = base64.b64encode(img_bytes).decode("utf-8")
        print("Sending to model...")
        
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:{img_format};base64,{img_b64}"}},
                    {"type": "text", "text": "Describe this image in detail."}
                ]
            }],
            max_tokens=1024,
            temperature=0.7
        )
        print("\n" + "="*60 + "\nModel Response:\n" + "="*60 + "\n")
        print(resp.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")


def test_multiple_images(image_urls):
    """测试多图理解 - 支持多个远程 URL 或本地文件路径"""
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        content = []
        
        # 处理每张图片
        for i, img_url in enumerate(image_urls, 1):
            if img_url.startswith("http"):
                headers = {"User-Agent": "Chrome/120.0.0.0 Safari/537.36"}
                resp = requests.get(img_url, headers=headers, verify=False, timeout=30)
                resp.raise_for_status()
                img_bytes = resp.content
            else:
                with open(img_url, "rb") as f:
                    img_bytes = f.read()
            
            img_format = mimetypes.guess_type(img_url)[0] or "jpeg"
            img_b64 = base64.b64encode(img_bytes).decode("utf-8")
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:{img_format};base64,{img_b64}"}
            })
        
        # 添加文本提示
        content.append({
            "type": "text",
            "text": "What are the key similarities and differences between these images?"
        })
        
        print(f"Sending {len(image_urls)} images to model...")
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": content}],
            max_tokens=1024,
            temperature=0.7
        )
        print("\n" + "="*60 + "\nModel Response:\n" + "="*60 + "\n")
        print(resp.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")


def test_video_understanding(video_url, output_path="video_output.txt"):
    """
    测试视频理解 - 使用 OpenAI 兼容 API
    
    Args:
        video_url: 视频文件的远程 URL 或本地文件路径
        output_path: 保存模型响应的输出文件路径
    """
    try:
        import base64
        import mimetypes
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # 获取视频数据
        if video_url.startswith("http"):
            print(f"Downloading video: {video_url}")
            headers = {"User-Agent": "Chrome/120.0.0.0 Safari/537.36"}
            resp = requests.get(video_url, headers=headers, verify=False, timeout=120)
            resp.raise_for_status()
            video_bytes = resp.content
        else:
            print(f"Loading local video: {video_url}")
            with open(video_url, "rb") as f:
                video_bytes = f.read()
        
        video_format = mimetypes.guess_type(video_url)[0] or "video/mp4"
        video_b64 = base64.b64encode(video_bytes).decode("utf-8")
        
        print(f"Sending video to model for understanding...")
        start_time = time.time()
        
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "video_url", "video_url": {"url": f"data:{video_format};base64,{video_b64}"}},
                    {"type": "text", "text": "このビデオで何が起きているか要約してください。主要な出来事とシーンを詳しく説明してください。"}
                ]
            }],
            max_tokens=1024,
            temperature=0.7
        )
        
        generation_time = time.time() - start_time
        result = resp.choices[0].message.content
        
        print("\n" + "="*60 + "\nVideo Understanding Result:\n" + "="*60 + "\n")
        print(result)
        print(f"\nGeneration Time: {generation_time:.2f} seconds")
        print("="*60)
        print("="*60)
        
    except Exception as e:
        print(f"\n⚠️  Video understanding error: {e}")
        print("\n解决方案:")
        print("1. 确保服务器已安装视频处理依赖（如 vllm[multimodal]）")
        print("2. 使用支持视频的模型（如 Gemma 4 E2B 或 E4B）")
        print("3. 当前使用的模型:", MODEL_NAME)
        return None


def test_audio_transcription(audio_path):
    try:
        # 读取音频文件
        print(f"Loading audio file: {audio_path}")
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        
        # 转为 base64
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        audio_format = mimetypes.guess_type(audio_path)[0] or "audio/ogg"
        
        print(f"Sending audio to model for transcription...")
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "audio_url", "audio_url": {"url": f"data:{audio_format};base64,{audio_b64}"}},
                    {"type": "text", "text": "Provide a verbatim, word-for-word transcription of the audio."}
                ]
            }],
            max_tokens=1024,
            temperature=0.7
        )
        print("\n" + "="*60 + "\nTranscription Result:\n" + "="*60 + "\n")
        print(resp.choices[0].message.content)
        return resp.choices[0].message.content
    except Exception as e:
        print(f"\n⚠️  Audio transcription error: {e}")
        print("\n解决方案:")
        print("1. 确保服务器已安装 vllm[audio] 依赖")
        print("2. 使用支持音频的模型（Gemma 4 E2B 或 E4B）")
        print("3. 当前使用的模型:", MODEL_NAME)


if __name__ == "__main__":
    # print("="*70)
    # print("Gemma 4 Model Test Suite")
    # print("="*70)
    
    # print("\n[TEST 1] Text Generation")
    # test_text_generation()
    
    # print("\n\n[TEST 2] Single Image Generation")
    # test_single_image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg")
    
    # print("\n\n[TEST 3] Multiple Images Generation")
    # image_urls = [
    #     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg",
    #     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/1200px-Cat_November_2010-1a.jpg"
    # ]
    # test_multiple_images(image_urls)
    
    # print("\n\n[TEST 4] Video Understanding")
    # print("="*70)
    
    # 测试视频理解
    # try:
    #     test_video_understanding("big-buck-bunny-480p-30sec.mp4")
    # except Exception as e:
    #     print(f"跳过视频测试：{e}")
    
    # print("\n\n[TEST 5] Audio Transcription (ASR)")
    # print("⚠️  注意：当前模型可能不支持音频功能")
    # print("="*70)
    
    # 尝试运行音频测试（如果支持）
    try:
        test_audio_transcription("こんにちは.ogg")
    except Exception as e:
        print(f"跳过音频测试：{e}")
    
    # print("\n" + "="*70)
    # print("Test Suite Completed")
    # print("="*70)
