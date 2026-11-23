from typing import Tuple, List
from app.utils.taxonomy import CRITICAL_TRIGGERS, HIGH_TRIGGERS, PRIORITY_LEVELS

class PriorityService:
    @staticmethod
    def evaluate_priority(text: str, category: str, detected_terms: List[str]) -> Tuple[str, float]:
        """
        Determines ticket priority level and corresponding SLA target in hours.
        Returns: (priority_name, sla_hours)
        """
        if not text:
            return "Medium", PRIORITY_LEVELS["Medium"]["sla_hours"]

        lower_text = text.lower()
        lower_terms = [t.lower() for t in detected_terms]

        # 1. Critical Priority Checks
        # - Any explicit critical phrases like 'production database', 'is down', 'datacenter down'
        is_critical_trigger = any(trigger in lower_text for trigger in CRITICAL_TRIGGERS)
        is_prod_down = ("production" in lower_text or "database" in lower_text or "server" in lower_text) and "down" in lower_text
        is_security_crisis = any(t in lower_terms for t in ["ransomware", "breach", "compromised"])

        if is_critical_trigger or is_prod_down or is_security_crisis:
            return "Critical", PRIORITY_LEVELS["Critical"]["sla_hours"]

        # 2. High Priority Checks
        # - Broad business impact or multiple users
        is_high_trigger = any(trigger in lower_text for trigger in HIGH_TRIGGERS)
        is_vpn_or_auth_block = "vpn" in lower_terms and ("down" in lower_terms or "cannot connect" in lower_text)

        if is_high_trigger or is_vpn_or_auth_block:
            return "High", PRIORITY_LEVELS["High"]["sla_hours"]

        # 3. Low Priority Checks
        # - Non-blocking requests, routine accessories, general queries
        low_indicators = ["request", "how to", "new mouse", "new keyboard", "headset replacement", "inquiry", "license renewal"]
        if any(ind in lower_text for ind in low_indicators) and "not" not in lower_text and "down" not in lower_text:
            return "Low", PRIORITY_LEVELS["Low"]["sla_hours"]

        # 4. Default to Medium Priority (e.g. single user laptop wi-fi or workstation issues)
        return "Medium", PRIORITY_LEVELS["Medium"]["sla_hours"]
