from fastapi import FastAPI, Request
from app.core.assistant import Brain
from app.memory.short_memory import short_mem

app = FastAPI()
memory = short_mem()
brain = Brain(short_memory=memory)

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data["message"]
    result = brain.Ask(user_message)
    return {
        "response": result["choices"][0]["message"]["content"]
    }
