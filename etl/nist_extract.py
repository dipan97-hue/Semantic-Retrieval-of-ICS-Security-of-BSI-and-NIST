# etl/nist_extractor.py

import fitz
import re

from etl.cleaning import (
    nist_clean_content,
    is_noise_title,
    is_bad_heading
)

from etl.chunking import split_into_chunks

from etl.common import (
    detect_normative,
    create_summary,
    extract_keywords
)

from etl.lifecycle_nist import extract_lifecycle


# ---------------------------------------------------
# LOAD PDF
# ---------------------------------------------------
def load_pdf_text(pdf_path):

    doc = fitz.open(pdf_path)

    full_text = ""

    for page in doc:
        full_text += "\n" + page.get_text()

    doc.close()

    return full_text


# ---------------------------------------------------
# MAIN NIST EXTRACTION
# ---------------------------------------------------
def extract_nist_chunks(pdf_path):

    # Load PDF
    full_text = load_pdf_text(pdf_path)

    # Remove front matter
    full_text = re.split(
        r"\n1\s+[A-Z]",
        full_text,
        maxsplit=1
    )[-1]

    # Remove table of contents
    full_text = re.sub(
        r"Table of Contents.*?(?=\n\d+\s+[A-Z])",
        "",
        full_text,
        flags=re.IGNORECASE | re.DOTALL
    )

    # Heading detection
    heading_pattern = re.compile(
        r"\n(\d+(?:\.\d+)*\.?)\s+([A-Z][A-Za-z0-9\(\)\-.,: ]{5,})"
    )

    matches = list(
        heading_pattern.finditer(full_text)
    )

    chunks_data = []

    seen_chunks = set()

    # ---------------------------------------------------
    # SECTION LOOP
    # ---------------------------------------------------
    for i, match in enumerate(matches):

        section_number = match.group(1).rstrip(".")

        title = match.group(2).strip()

        # Skip noisy headings
        if is_noise_title(title) or is_bad_heading(title):
            continue

        # Section boundaries
        start = match.end()

        end = (
            matches[i + 1].start()
            if i + 1 < len(matches)
            else len(full_text)
        )

        raw_content = full_text[start:end]

        # Clean content
        content = nist_clean_content(raw_content)

        if not content:
            continue

        # Skip noisy blocks
        if any(x in content.lower() for x in [
            "see table",
            "see figure",
            "see section",
            "acronym",
            "abbreviation"
        ]):
            continue

        # Skip figure-heavy sections
        if re.search(r"\bfig(?:ure)?\.?\s*\d+", content.lower()):
            continue

        # Normative detection
        normative_flag, norm_type = detect_normative(content)

        # Skip weak content
        if not normative_flag and len(content) < 120:
            continue

        # Metadata
        summary = create_summary(content)

        keywords = extract_keywords(content)

        # Chunking
        chunks = split_into_chunks(content)

        # ---------------------------------------------------
        # CHUNK LOOP
        # ---------------------------------------------------
        for idx, chunk in enumerate(chunks):

            if chunk in seen_chunks:
                continue

            seen_chunks.add(chunk)

            lifecycle = extract_lifecycle(chunk)

            chunk_obj = {
                "source_standard": "NIST",
                "source_id": f"NIST-{section_number}",
                "section_number": section_number,
                "title": title,
                "parent": (
                    section_number.rsplit(".", 1)[0]
                    if "." in section_number
                    else None
                ),
                "chunk_id": f"NIST_{section_number}_{idx}",
                "content": chunk,
                "summary": summary,
                "keywords": keywords,
                "lifecycle_phase": lifecycle,
                "normative": normative_flag,
                "normative_type": norm_type
            }

            chunks_data.append(chunk_obj)

    return chunks_data