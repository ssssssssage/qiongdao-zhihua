import os
import requests
import json

api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.tu-zi.com/v1")
model = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")

if not api_key:
    print("❌ 没有读取到 DEEPSEEK_API_KEY")
    raise SystemExit

url = base_url.rstrip("/") + "/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

payload = {
    "model": model,
    "messages": [
        {
            "role": "system",
            "content": "你是一个测试助手，只输出简短中文。"
        },
        {
            "role": "user",
            "content": "请回复：API测试成功。"
        }
    ],
    "stream": False
}

print("请求地址：", url)
print("模型名称：", model)

try:
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    print("状态码：", response.status_code)
    print("原始返回：")
    print(response.text)

    response.raise_for_status()

    data = response.json()
    print("\n解析后的回复：")
    print(data["choices"][0]["message"]["content"])

except Exception as e:
    print("❌ API测试失败：", repr(e))