import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

faqs = []

# Load FAQ data (one JSON per line)
with open("data/customer_support_faqs.json", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            faqs.append(json.loads(line))

questions = [faq["question"] for faq in faqs]
answers = [faq["answer"] for faq in faqs]

# Vectorize FAQ questions
vectorizer = TfidfVectorizer(stop_words="english")
faq_vectors = vectorizer.fit_transform(questions)

def find_faq_answer(query, threshold=0.3):
    query = query.lower().strip()
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, faq_vectors)[0]

    best_idx = similarities.argmax()
    best_score = similarities[best_idx]

    # Return answer only if similarity is high enough
    if best_score >= threshold:
        return answers[best_idx]

    return None



