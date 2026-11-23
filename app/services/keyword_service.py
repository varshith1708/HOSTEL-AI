import re
from typing import List
from app.utils.taxonomy import CATEGORIES

ALL_TECHNICAL_TERMS = [
    # Multi-word compound terms
    "production database", "packet loss",
    "docking station", "power adapter", "active directory", "password reset",
    "password expired", "account locked", "permission denied", "access request",
    "suspicious email", "credential leak", "security alert", "data leak",
    "virtual machine", "cpu spike", "disk full", "software update",

    # Key tech nouns & verbs
    "wi-fi", "wifi", "ethernet", "vpn", "connecting", "connection", "connect",
    "dns", "gateway", "router", "switch", "broadband", "internet", "lan", "wlan",
    "database", "server", "cluster", "kubernetes", "k8s", "aws", "azure", "gcp",
    "redis", "postgres", "mysql", "down", "outage", "host", "storage",
    "laptop", "desktop", "monitor", "keyboard", "battery", "charger", "mouse", "printer",
    "crash", "bug", "slack", "teams", "outlook", "excel", "browser", "chrome",
    "phishing", "malware", "ransomware", "breach", "virus", "sso", "okta", "mfa"
]

class KeywordService:
    @staticmethod
    def extract_detected_terms(text: str) -> List[str]:
        """
        Extracts key technical terms and action verbs present in the text,
        preserving the original casing from user input.
        """
        if not text:
            return []

        detected = []
        lower_text = text.lower()

        # Sort candidate terms by length descending to match longest phrases first
        sorted_candidates = sorted(ALL_TECHNICAL_TERMS, key=len, reverse=True)

        matched_intervals = []

        for candidate in sorted_candidates:
            # Match word boundary or hyphenated boundary
            pattern = r"(?<!\w)" + re.escape(candidate) + r"(?!\w)"
            for match in re.finditer(pattern, lower_text):
                start, end = match.span()
                # Check for overlap with already matched longer phrases
                overlap = any(s <= start < e or s < end <= e for s, e in matched_intervals)
                if not overlap:
                    matched_intervals.append((start, end))
                    original_word = text[start:end]
                    # Normalize casing for canonical terms like Wi-Fi
                    if original_word.lower() in ["wi-fi", "wifi"]:
                        display_term = "Wi-Fi"
                    else:
                        display_term = original_word
                    if display_term not in detected:
                        detected.append(display_term)

        return detected
