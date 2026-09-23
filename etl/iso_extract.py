import re
import fitz

from etl.chunking import split_into_chunks
from etl.common import (
    detect_normative,
    create_summary,
    extract_keywords
)
from etl.cleaning import  is_noise_title, is_reference_section, clean_iso

# ============================================================
# LOAD PDF
# ============================================================

def load_pdf_text(pdf_path):

    doc = fitz.open(pdf_path)

    try:

        pages = []

        for page_number, page in enumerate(doc, start=1):

            text = page.get_text()

            if text:
                pages.append(
                    f"\n[PAGE {page_number}]\n{text}"
                )

        return "\n".join(pages)

    finally:

        doc.close()


# ============================================================
# CLEAN ISO CONTENT
# ============================================================

def clean_iso_content(text):

    if not text:
        return ""

    # Remove page markers
    text = re.sub(
        r"\[PAGE\s+\d+\]",
        "",
        text
    )

    # Normalize whitespace
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Normalize excessive blank lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


# ============================================================
# DETECT ISO SECTION HEADINGS
# ============================================================

def detect_iso_sections(full_text):

    """
    Detect headings such as:

    1 Scope
    4 General considerations
    8 Cybersecurity management
    8.3 Cybersecurity monitoring
    15 Threat analysis and risk assessment methods
    15.3 Asset identification

    """

    pattern = re.compile(
        r"(?m)^\s*"
        r"(\d+(?:\.\d+)*)"
        r"\s+"
        r"([A-Z][^\n]+)"
        r"\s*$"
    )

    matches = list(pattern.finditer(full_text))

    return matches


# ============================================================
# EXTRACT ISO/SAE 21434 CHUNKS
# ============================================================

def extract_iso_chunks(pdf_path):

    full_text = load_pdf_text(pdf_path)

    matches = detect_iso_sections(full_text)

    chunks_data = []

    seen_chunks = set()

    for i, match in enumerate(matches):

        section_number = match.group(1).strip()

        title = match.group(2).strip()

        # ----------------------------------------------------
        # Ignore obvious non-section text
        # ----------------------------------------------------

        if len(title) < 3:
            continue

        # ----------------------------------------------------
        # Only ISO clauses
        #
        # ISO/SAE 21434 contains numbered clauses such as:
        # 1
        # 2
        # 3
        # 4
        # ...
        # 15.3
        #
        # ----------------------------------------------------

        start = match.end()

        if i + 1 < len(matches):

            end = matches[i + 1].start()

        else:

            end = len(full_text)

        raw_content = full_text[start:end]

        content = clean_iso_content(raw_content)

        content = clean_iso(content)

        if not content:
            continue

        # ----------------------------------------------------
        # Detect normative language
        # ----------------------------------------------------

        normative_flag, norm_type = detect_normative(
            content
        )

        # ----------------------------------------------------
        # Summary
        # ----------------------------------------------------

        summary = create_summary(content)

        # ----------------------------------------------------
        # Keywords
        # ----------------------------------------------------

        keywords = extract_keywords(content)

        # ----------------------------------------------------
        # Chunk large sections
        # ----------------------------------------------------

        chunks = split_into_chunks(content)

        for idx, chunk in enumerate(chunks):

            chunk = chunk.strip()

            if not chunk:
                continue

            if chunk in seen_chunks:
                continue

            seen_chunks.add(chunk)

            # ------------------------------------------------
            # Chunk ID
            # ------------------------------------------------

            chunk_id = (
                f"ISO21434_"
                f"{section_number.replace('.', '_')}_"
                f"{idx}"
            )

            # ------------------------------------------------
            # Parent section
            # ------------------------------------------------

            if "." in section_number:

                parent = section_number.rsplit(
                    ".",
                    1
                )[0]

            else:

                parent = None

            # ------------------------------------------------
            # Add record
            # ------------------------------------------------

            chunks_data.append({

                "source_standard":
                    "ISO/SAE 21434",

                "source_id":
                    f"ISO21434-{section_number}",

                "section_number":
                    section_number,

                "title":
                    title,

                "parent":
                    parent,

                "chunk_id":
                    chunk_id,

                "content":
                    chunk,

                "summary":
                    summary,

                "keywords":
                    keywords,

                "lifecycle_phase":
                    "Automotive Cybersecurity Lifecycle",

                "normative":
                    normative_flag,

                "normative_type":
                    norm_type

            })

    return chunks_data