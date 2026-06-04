import re
import nltk

## Normative references

def detect_normative(text):
    text_lower = text.lower()

    if 'shall' in text_lower:
        return True, 'shall'
    if 'may' in text_lower:
        return True, 'may'
    if 'should' in text_lower:
        return True, 'should'
    return False, None
    
## Create summary 
def create_summary(text, max_sentences=2):

    try:
        sentences = nltk.sent_tokenize(text)
    except LookupError:
        # Newer NLTK versions may require punkt_tab in addition to punkt.
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        sentences = nltk.sent_tokenize(text)

    return " ".join(sentences[:max_sentences])

## Keyword Extraction
def extract_keywords(text, max_keywords=5):

    words = re.findall(r'\b[a-zA-Z]{6,}\b', text.lower())

    freq = {}

    for w in words:
        freq[w] = freq.get(w, 0) + 1

    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    return [w[0] for w in sorted_words[:max_keywords]]
