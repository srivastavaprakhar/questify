from openai import OpenAI
import os   

class ShivaayEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("SHIVAAY_API_KEY")
        if not self.api_key:
            raise ValueError("❌ SHIVAAY_API_KEY not found. Please set it in your .env file.")

        # Shivaay API base
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.futurixai.com/api/shivaay/v1"
        )

    def generate(self, prompt: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model="shivaay",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Error from Shivaay API: {e}"
