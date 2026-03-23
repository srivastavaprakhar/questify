import os
import requests

class ShivaayEngine:

    def __init__(self):
        self.api_key = os.getenv("SHIVAAY_API_KEY")
        self.url = "https://ai.futurixai.com/v1/chat/completions"

    def generate(self, prompt: str):

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "shivaay",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }

        r = requests.post(self.url, headers=headers, json=payload)

        if r.status_code != 200:
            return f"Error from Shivaay API: {r.status_code} - {r.text}"

        return r.json()["choices"][0]["message"]["content"]