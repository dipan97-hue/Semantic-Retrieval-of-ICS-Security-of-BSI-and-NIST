# etl/cleaning.py

import re

# ---------------------------------------------------
# BOX CHARACTERS
# ---------------------------------------------------
BOX_CHARS = "┌┐└┘├┤┬┴┼│─═║╔╗╚╝╠╣╦╩╬█▄▀"


# ---------------------------------------------------
# NOISE TITLE FILTER
# ---------------------------------------------------
def is_noise_title(title):

    if not title:
        return True

    t = title.lower().strip()

    return any(x in t for x in [
        "introduction",
        "overview",
        "document",
        "structure",
        "appendix",
        "reference",
        "figure",
        "fig",
        "table",
        "acronym",
        "glossary",
        "abbreviation",
        "table of contents"
    ])

## Referencing sections are often normative but contain no useful content, so we filter them out early
def is_reference_section(section_number: str, title: str) -> bool:
    title_lower = title.lower().strip()
    return (
        section_number.startswith("11.1")
        or "reference" in title_lower
    )


# ---------------------------------------------------
# BAD HEADING FILTER
# ---------------------------------------------------
def is_bad_heading(title):

    if not title:
        return True

    t = title.strip()

    # headings like AC-1
    if re.fullmatch(r"[A-Z]{1,5}-\d+", t):
        return True

    # headings like A.1.2
    if re.fullmatch(r"[A-Z]\.\d+(\.\d+)*\.?", t):
        return True

    # broken refs
    if "see https:" in t.lower():
        return True

    # TOC style headings
    if "..." in t:
        return True

    # too short
    if len(t) < 8:
        return True

    return False


# ---------------------------------------------------
# BSI CLEANING
# ---------------------------------------------------
def bsi_clean_content(text: str) -> str:

    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:

        stripped = line.strip()

        if not stripped:
            continue

        # Remove page numbers
        if re.fullmatch(r"Page\s+\d+", stripped, flags=re.IGNORECASE):
            continue

        # Remove TOC
        if re.search(r"Table of contents", stripped, flags=re.IGNORECASE):
            continue

        # Remove BSI headers
        if re.search(
            r"Federal Office for Information Security",
            stripped,
            flags=re.IGNORECASE
        ):
            continue

        # Remove copyright
        if re.search(r"Copyright", stripped, flags=re.IGNORECASE):
            continue

        # Remove BSI title headers
        if re.search(r"BSI Standard 200-1", stripped, flags=re.IGNORECASE):
            continue

        # Remove standalone numbers
        if re.fullmatch(r"\d+", stripped):
            continue

        # Remove box chars
        if any(ch in BOX_CHARS for ch in stripped):
            continue

        cleaned_lines.append(stripped)

    # IMPORTANT: outside loop
    cleaned = " ".join(cleaned_lines)

    # Remove control chars
    cleaned = re.sub(r"[\x00-\x1f\x7f]", " ", cleaned)

    # Fix broken words
    cleaned = re.sub(
        r"(\b[\w]{2,})-\s+([\w]{2,}\b)",
        r"\1\2",
        cleaned
    )

    # Remove extra spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


# ---------------------------------------------------
# NIST CLEANING
# ---------------------------------------------------
def nist_clean_content(text: str) -> str:

    # remove non-ascii
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # remove citations
    text = re.sub(r"\[[^\]]+\]", " ", text)

    # remove figures
    text = re.sub(
        r"\bfig(?:ure)?\.?\s*\d+\.?",
        " ",
        text,
        flags=re.IGNORECASE
    )

    # remove tables
    text = re.sub(
        r"\btable\s*\d+\.?",
        " ",
        text,
        flags=re.IGNORECASE
    )

    # remove see references
    text = re.sub(
        r"\bsee\s+(table|figure|section|https?)\S*",
        " ",
        text,
        flags=re.IGNORECASE
    )

    # remove acronym references
    text = re.sub(
        r"\b[A-Z]{2,}\s*\([A-Z]{2,}\)",
        " ",
        text
    )

    # fix broken words
    text = re.sub(
        r"(\b[\w]{2,})-\s+([\w]{2,}\b)",
        r"\1\2",
        text
    )

    # remove legal refs
    text = re.sub(
        r"\bstat\.\s*\d+",
        " ",
        text,
        flags=re.IGNORECASE
    )

    # remove broken URL fragments
    text = re.sub(r"https?:\S*", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text