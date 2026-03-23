import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = "C:/Users/Prakhar Srivastava/Desktop/PROJECTS/AskQuery/models/Mistral/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
DB_PATH = "database/trial1.db"
INDEX_PATH = "faiss_index"

SHIVAAY_API_KEY = os.getenv("SHIVAAY_API_KEY")