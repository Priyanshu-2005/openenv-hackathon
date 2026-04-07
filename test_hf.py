import requests
import os
headers = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}
url = "https://router.huggingface.co/hf-inference/v1/chat/completions"
data = {"model": "Qwen/Qwen2.5-72B-Instruct", "messages": [{"role": "user", "content": "hello"}]}
r = requests.post(url, headers=headers, json=data)
print(r.status_code, r.text)
