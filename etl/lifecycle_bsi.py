from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


LIFECYCLE_DESCRIPTIONS = {
    "Plan": "planning strategy risk assessment objectives policies governance preparation",
    "Do": "implementation execution security controls operational processes deployment",
    "Check": "audit monitoring review evaluation performance compliance verification",
    "Act": "improvement corrective actions optimization continuous improvement"
}

vectorizer = TfidfVectorizer()

phase_names = list(LIFECYCLE_DESCRIPTIONS.keys())
phase_texts = list(LIFECYCLE_DESCRIPTIONS.values())

phase_vectors = vectorizer.fit_transform(phase_texts)


def extract_bsi_lifecycle(text):

    text_vector = vectorizer.transform([text])

    similarities = cosine_similarity(text_vector, phase_vectors)[0]

    best_match = phase_names[similarities.argmax()]

    return best_match