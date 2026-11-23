import re
from typing import List

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "because", "as", "what",
    "which", "this", "that", "these", "those", "then", "just", "so", "than",
    "such", "both", "through", "about", "for", "is", "of", "while", "during",
    "to", "from", "in", "out", "on", "off", "again", "further", "then", "once"
}

def clean_text(text: str) -> str:
    """Normalize text by converting to lowercase and stripping extra whitespace."""
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

def extract_tokens(text: str) -> List[str]:
    """Tokenize words and hyphenated terms."""
    if not text:
        return []
    cleaned = clean_text(text).lower()
    tokens = re.findall(r"\b[a-z0-9]+(?:-[a-z0-9]+)*\b", cleaned)
    return [t for t in tokens if t not in STOPWORDS]

def find_matched_spans(text: str, candidate_terms: List[str]) -> List[str]:
    """
    Search original text for matching candidate terms, preserving original casing.
    Handles hyphenated terms (e.g. Wi-Fi) and multi-word phrases.
    """
    if not text or not candidate_terms:
        return []

    detected = []
    lower_text = text.lower()

    # Sort candidates by length descending to match compound terms first
    sorted_terms = sorted(candidate_terms, key=len, reverse=True)

    for term in sorted_terms:
        pattern = r"\b" + re.escape(term.lower()) + r"\b"
        match = re.search(pattern, lower_text)
        if match:
            # Extract verbatim matching text slice from original text
            start, end = match.span()
            matched_slice = text[start:end]
            if matched_slice not in detected:
                detected.append(matched_slice)

    return detected
