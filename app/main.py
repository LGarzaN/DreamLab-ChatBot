from fastapi import FastAPI
from pydantic import BaseModel

from chatbot import chat

app = FastAPI()

class ChatRequest(BaseModel):
    session_id: str
    prompt: str

@app.post("/chat/")
async def chat_endpoint(chat_request: ChatRequest):
    response = chat(chat_request.session_id, chat_request.prompt)
    return {"response": response, "session_id": chat_request.session_id}
