from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import json
import os
import requests
from dotenv import load_dotenv

OPENROUTER_API_KEY="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"

# Load environment variables from .env (if available)
load_dotenv()

# FastAPI App
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# React build path
frontend_path = os.path.join(os.path.dirname(__file__), "frontend/build")

# Serve static files
app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

# Root route to serve index.html
@app.get("/")
def serve_react_app():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# React Router fallback
@app.get("/{full_path:path}")
def serve_react_router(full_path: str):
    if full_path.startswith("docs") or full_path.startswith("openapi.json"):
        return {"message": "API documentation route"}
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "React app not built. Please run `npm run build` in frontend."}

# ------------------- API ROUTES -------------------

@app.get("/profile")
def get_profile():
    with open("profiles.json", "r") as f:
        return json.load(f)

@app.get("/goals")
def get_goals():
    with open("chat_logs/devuser/goals.json", "r") as f:
        return json.load(f)

@app.get("/insights")
def get_insights():
    with open("chat_logs/devuser/goals.json", "r") as f:
        goals = json.load(f)
        return [g["insight"] for g in goals if "insight" in g]

@app.get("/chat")
def get_chat():
    with open("chat_logs/devuser/history.json", "r") as f:
        return json.load(f)

@app.get("/ping")
def ping():
    return {"message": "pong"}

# ------------------- MODELS -------------------

class Memory(BaseModel):
    username: str
    text: str
    emotion: str
    cognition: str
    label: str
    theme: str
    timestamp: str
    linked_goals: list[str]

class Goal(BaseModel):
    username: str
    goal: str
    status: str
    created_at: str

class ChatRequest(BaseModel):
    username: str
    text: str

# ------------------- POST ROUTES -------------------

@app.post("/memories")
def save_memory(memory: Memory):
    user_dir = f"chat_logs/{memory.username}"
    os.makedirs(user_dir, exist_ok=True)
    file_path = os.path.join(user_dir, "history.json")

    data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)

    data.append(memory.dict())

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    return {"status": "success", "message": "Memory saved"}

@app.post("/goals")
def save_goal(goal: Goal):
    user_dir = f"chat_logs/{goal.username}"
    os.makedirs(user_dir, exist_ok=True)
    file_path = os.path.join(user_dir, "goals.json")

    data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)

    data.append(goal.dict())

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    return {"status": "success", "message": "Goal saved"}

@app.post("/chat")
def chat_with_ai(chat: ChatRequest):
    prompt = chat.text.strip()
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return {"reply": "⚠️ OPENROUTER_API_KEY is missing in environment variables."}

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "system", "content": "You are a thoughtful, helpful AI."},
                    {"role": "user", "content": prompt}
                ]
            }
        )
        reply = response.json()["choices"][0]["message"]["content"]
        return {"reply": reply}

    except Exception as e:
        print("❌ Chat API error:", e)
        return {"reply": "⚠️ AI failed to respond. Check server logs."}

# ------------------- MAIN -------------------

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8080)
