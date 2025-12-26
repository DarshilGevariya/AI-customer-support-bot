# AI Customer Support Bot

## Project Overview
This project simulates an AI-based customer support system that answers user queries using a FAQ knowledge base and escalates queries when required.  
It maintains session-based conversation memory and integrates a Large Language Model (LLM) for generating responses when FAQs are insufficient.

---

## Scope of Work
- Input handling for FAQs and customer queries  
- Contextual memory across conversations  
- Escalation for unanswered or sensitive queries  
- Backend API for interaction  

---

## Tech Stack
- **Backend:** FastAPI  
- **LLM:** Google FLAN-T5 (Hugging Face Inference API)  
- **Database:** SQLite (SQLAlchemy)  
- **NLP:** TF-IDF, Cosine Similarity  
- **Language:** Python  

---

## Prompt Design & LLM Usage
The LLM is instructed to act as a customer support assistant and generate clear, concise responses.  
User queries are first matched against FAQs using similarity scoring.  
If no suitable FAQ is found, the query along with conversation history is passed to the LLM.

---

## Escalation Logic
A query is escalated when:
- No relevant FAQ match is found, and  
- The query contains sensitive or internal keywords  

---

## Session Management
Each interaction is stored with a session ID, user message, bot response, and timestamp to maintain conversational context.

---

## API Endpoints
- **POST `/start-session`** – Starts a new session  
- **POST `/chat`** – Accepts session ID and message, returns response and escalation status  

---

## How to Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
