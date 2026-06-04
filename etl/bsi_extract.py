import re
from etl.chunking import split_into_chunks
from etl.lifecycle_bsi import extract_bsi_lifecycle as extract_lifecycle
import fitz
from etl.common import detect_normative, create_summary, extract_keywords
from etl.cleaning import is_noise_title,  is_noise_title, is_reference_section, bsi_clean_content
from etl.lifecycle_bsi import extract_bsi_lifecycle



def load_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    try:
        return "".join("\n" + page.get_text() for page in doc)
    finally:
        doc.close()

def extract_bsi_chunks(pdf_path):
    full_text = load_pdf_text(pdf_path)
    heading_pattern = re.compile(r"\n((\d+(?:\.\d+)*)\s+([A-Z][^\n]+))")
    matches = list(heading_pattern.finditer(full_text))

    chunks_data = []
    seen_chunks = set()

    for i, match in enumerate(matches):
        section_number = match.group(2)
        title = match.group(3).strip()

        # Skip unwanted sections
        if is_reference_section(section_number, title):
            continue
        if section_number.isdigit() and int(section_number) > 20:
            continue
        if re.fullmatch(r"V\s+\d+(?:\.\d+)*", title):
            continue
        if is_noise_title(title):
            continue

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)

        raw_content = full_text[start:end]
        content = bsi_clean_content(raw_content)

        if not content:
            continue

        # IMPORTANT: detect normative BEFORE chunking
        normative_flag, norm_type = detect_normative(content)

        # Skip weak sections early
        if norm_type not in ["shall", "should"]:
            continue

        lifecycle = extract_lifecycle(title + " " + content)
        keywords = extract_keywords(content)
        summary = create_summary(content)
        chunks = split_into_chunks(content)

        for idx, chunk in enumerate(chunks):
            if chunk in seen_chunks:
                continue
            seen_chunks.add(chunk)

            chunks_data.append({
                "source_standard": "BSI",
                "source_id": f"BSI-{section_number}",
                "section_number": section_number,
                "title": title,
                "parent": section_number.rsplit(".", 1)[0] if "." in section_number else None,
                "chunk_id": f"BSI_{section_number}_{idx}",
                "content": chunk,
                "summary": summary,
                "keywords": keywords,
                "lifecycle_phase": lifecycle,
                "normative": normative_flag,
                "normative_type": norm_type
            })

    return chunks_data
