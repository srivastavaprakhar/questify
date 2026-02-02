from llama_cpp import Llama
import os

class MistralEngine:
    def __init__(self, model_path: str):
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,           # Reduced context
            n_threads=4,          # Fixed to 4 threads
            n_batch=8,            # Add batch size if possible
            temperature=0.2,
            top_p=0.9,
            stop=["</s>"]
        )

    def generate(self, prompt: str) -> str:
        output = self.llm(
            prompt,
            max_tokens=512,
        )
        return output['choices'][0]['text'].strip()
