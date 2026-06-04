from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
LIFECYCLE_DESCRIPTIONS = {
    "Identify": "risk asset inventory governance assessment",
    "Protect": "access control protection encryption safeguards",
    "Detect": "monitor detection logging anomaly detection",
    "Respond": "incident response mitigation communication",
    "Recover": "recovery restore backup resilience"
}

vectorizer = TfidfVectorizer()
phase_names = list(LIFECYCLE_DESCRIPTIONS.keys())
phase_vectors = vectorizer.fit_transform(LIFECYCLE_DESCRIPTIONS.values())

def extract_lifecycle(text, threshold=0.15):
    text_vector = vectorizer.transform([text])
    similarities = cosine_similarity(text_vector, phase_vectors)[0]

    best_idx = similarities.argmax()

    if similarities[best_idx] < threshold:
        return None

    return phase_names[best_idx]