from typing import List
from app.utils.taxonomy import CATEGORIES

class RoutingService:
    @staticmethod
    def determine_team(category: str, priority: str, detected_terms: List[str], text: str = "") -> str:
        """
        Routes the analyzed ticket to the appropriate IT specialist team.
        """
        lower_text = text.lower() if text else ""
        lower_terms = [t.lower() for t in detected_terms]

        # Critical database or cloud infrastructure always routes to IT Infrastructure
        if "production database" in lower_text or "database" in lower_terms:
            if "down" in lower_terms or "server" in lower_terms or priority in ["Critical", "High"]:
                return "IT Infrastructure"

        # Check category mapping
        if category in CATEGORIES:
            return CATEGORIES[category]["default_team"]

        # Fallback routing based on keywords
        if any(w in lower_terms for w in ["wi-fi", "wifi", "ethernet", "router", "vpn", "connecting"]):
            return "IT Network Team"

        if any(w in lower_terms for w in ["database", "server", "aws", "cluster", "down"]):
            return "IT Infrastructure"

        if any(w in lower_terms for w in ["laptop", "monitor", "battery", "charger", "keyboard"]):
            return "Hardware Support"

        if any(w in lower_terms for w in ["phishing", "malware", "ransomware", "breach"]):
            return "Security Operations Center (SOC)"

        return "Helpdesk Tier 1"
