import google.generativeai as genai
import os

class GeminiEngine:

    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-3-flash-preview")

    def generate(self, prompt: str):

        response = self.model.generate_content(prompt)

        return response.text.strip()