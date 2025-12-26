import requests

MODEL_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

def generate_response(conversation, user_query):
    # Prompt passed to the LLM
    prompt = f"""
You are a helpful customer support assistant.

Answer the user's question clearly and concisely.

Conversation so far:
{conversation}

Question:
{user_query}
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.3
        }
    }

    try:
        response = requests.post(MODEL_URL, json=payload, timeout=30)
        output = response.json()

        # flan-t5 returns list of dicts with generated_text
        if isinstance(output, list) and "generated_text" in output[0]:
            return output[0]["generated_text"].strip()

    except Exception:
        pass

    # Safe fallback (very rare)
    return "I'm sorry, I couldn't retrieve the information right now."
