from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import json
import os

app = FastAPI()

# Allow frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to ["http://localhost:3000"] in dev if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to React production build
frontend_path = os.path.join(os.path.dirname(__file__), "frontend/build")

# Serve static assets
app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

# Serve React index.html for root
@app.get("/")
def serve_react_app():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Catch-all for React Router (e.g. /profile, /goals)
@app.get("/{full_path:path}")
def serve_react_router(full_path: str):
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

# ------------------- MAIN -------------------

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8080)

