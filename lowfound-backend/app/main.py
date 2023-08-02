from fastapi import FastAPI, WebSocket,Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import ai_api

app = FastAPI()
import time


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

questions = []

# Add questions
@app.post("/ask-question", tags=["questions"])
async def add_question(card: dict) -> dict:
    
    last_id = 1
    if (len(questions) != 0):
        last_id = questions[ len(questions) - 1]['id'] 
        
    questions.append({ 
        "id": last_id + 1,
        "date":card['date'],
        "question":card['question'],
        "answer":ai_api.send_question(card['question'])}) 
    return {
        "data": { "Question added." }
    }

# Get all todos
@app.get("/questions", tags=["todos"])
async def get_questions() -> dict:
    return { "data": questions }

@app.delete("/questions")
async def delete_item():
    # Your code to delete the item with the given item_id
    questions.clear()
    return {"message": f"DB has been deleted"}



