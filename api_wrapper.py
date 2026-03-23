from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import suppress_output  # ✅ reuse the same context manager
from main import answer_question, safe_llm_init
from embed_and_index import build_index
from auth.user_auth import signup, login, init_user_table
from config import DB_PATH, INDEX_PATH
import logging
import os
import logging
from fastapi.middleware.cors import CORSMiddleware

# Silence noisy loggers
logging.getLogger("watchdog").setLevel(logging.WARNING)

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/system.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
logger = logging.getLogger()

# ==== FastAPI App ====
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace * with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== Init DB ====
os.makedirs("database", exist_ok=True)
init_user_table()

# ==== Load once ====
with suppress_output():
   model = safe_llm_init()
   index = build_index(db_path=DB_PATH, persist_path=INDEX_PATH)

# ==== Request Models ====
class AuthRequest(BaseModel):
    username: str
    password: str

class QuestionRequest(BaseModel):
    question: str

# ==== API Routes ====

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/signup")
def api_signup(data: AuthRequest):
    if signup(data.username, data.password):
        logger.info(f"User '{data.username}' signed up via API")
        return {"status": "Signup successful"}
    else:
        logger.warning(f"Signup failed: Username '{data.username}' already exists.")
        raise HTTPException(status_code=400, detail="Username already exists.")

@app.post("/login")
def api_login(data: AuthRequest):
    if login(data.username, data.password):
        logger.info(f"User '{data.username}' logged in via API")
        return {"status": "Login successful"}
    else:
        logger.warning(f"Login failed for user '{data.username}'")
        raise HTTPException(status_code=401, detail="Invalid credentials.")

@app.post("/ask")
def api_ask(req: QuestionRequest):
    try:
        response = answer_question(index, req.question, model)
        logger.info(f"Question: {req.question} → Answer: {response}")
        return {"answer": response}
    except Exception as e:
        logger.exception("Error while answering question.")
        raise HTTPException(status_code=500, detail="Error generating response")
    
# ==== Dev server entry ====
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_wrapper:app", host="127.0.0.1", port=8000, reload=False)
