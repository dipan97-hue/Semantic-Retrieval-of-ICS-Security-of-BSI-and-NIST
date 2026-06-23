import re

def split_into_chunks( text, chunk_size=350,overlap=75):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join( words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks