import re
def split_into_chunks(text, max_sentences=2):
    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    for i in range(0, len(sentences), max_sentences):
        chunk = " ".join(sentences[i:i + max_sentences]).strip()

        if len(chunk) > 100:
            chunks.append(chunk)

    return chunks

