from fastapi import FastAPI
from pydantic import BaseModel
import uuid

from app.db import SessionLocal, ChatSession
from app.faq import find_faq_answer
from app.llm import generate_response

app = FastAPI(title="AI Customer Support Bot")

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/start-session")
# Generate a new session ID
def start_session():
    return {"session_id": str(uuid.uuid4())}

@app.post("/chat")
def chat(req: ChatRequest):
    db = SessionLocal() 

    # Fetch previous conversation for this session
    history = db.query(ChatSession).filter(
        ChatSession.session_id == req.session_id
    ).all()

    conversation = "\n".join(
        [f"User: {h.user_message}\nBot: {h.bot_response}" for h in history]
    )

    escalated = False

    # Try FAQ-based answer first
    faq_answer = find_faq_answer(req.message)

    if faq_answer is not None:
        bot_response = faq_answer
        escalated = False

    else:
        # Fall back to LLM if no FAQ match
        bot_response = generate_response(conversation, req.message)
        
        # Escalate on sensitive/internal queries
        user_msg = req.message.lower()
        sensitive_keywords = [
            "internal", "algorithm", "fraud",
            "confidential", "security", "backend"
        ]

        if any(word in user_msg for word in sensitive_keywords):
            bot_response = "I’m escalating this issue to a human support agent."
            escalated = True

    # Store interaction in database
    record = ChatSession(
        id=str(uuid.uuid4()),
        session_id=req.session_id,
        user_message=req.message,
        bot_response=bot_response
    )

    db.add(record)
    db.commit()

    return {
        "response": bot_response,
        "escalated": escalated
    }

