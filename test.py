import sys
import requests
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QDialog
api = "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"
prompt = ""
model = "openai/gpt-oss-120b:free"

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",  # ← правильный эндпоинт
    headers={
        "Authorization": f"Bearer {api}",  # ← обязательно Bearer
        "Content-Type": "application/json",
    },
    json={
        "model": f"{model}",
        "messages": [  # ← messages вместо input
            {"role": "user", "content": f"Hi"}
        ],
        "max_tokens": 9000,  # ← max_tokens, а не max_output_tokens
    }
)

result = response.json()
print(result['choices'][0]['message']['content'])