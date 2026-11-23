import time
from typing import Dict, Any
from app.services.keyword_service import KeywordService
from app.services.classification_service import ClassificationService
from app.services.priority_service import PriorityService
from app.services.routing_service import RoutingService
from app.models.ticket import AnalysisLog
from app.utils.extensions import db

class AnalyzerService:
    @classmethod
    def analyze_ticket(cls, text: str, save_log: bool = False) -> Dict[str, Any]:
        """
        Master pipeline:
        1. Extracts detected technical terms
        2. Categorizes incident & estimates confidence
        3. Evaluates priority & SLA target
        4. Determines routing team
        5. Formats standardized output structure
        """
        start_time = time.perf_counter()

        if not text or not text.strip():
            return {
                "error": "Input text cannot be empty",
                "category": "Unknown",
                "priority": "Low",
                "assigned_team": "Helpdesk Tier 1",
                "confidence": 0.0,
                "confidence_pct": "0.0%",
                "detected_terms": [],
                "sla_hours": 24.0,
                "response_time_ms": 0.0
            }

        # Step 1: Detect technical key terms and action verbs
        detected_terms = KeywordService.extract_detected_terms(text)

        # Step 2: Categorization & Confidence estimation
        category, confidence, score_breakdown = ClassificationService.classify(text, detected_terms)

        # Step 3: Priority evaluation & SLA target
        priority, sla_hours = PriorityService.evaluate_priority(text, category, detected_terms)

        # Step 4: Routing team assignment
        assigned_team = RoutingService.determine_team(category, priority, detected_terms, text)

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        result = {
            "input_text": text,
            "category": category,
            "priority": priority,
            "assigned_team": assigned_team,
            "confidence": round(confidence, 4),
            "confidence_pct": f"~{int(round(confidence * 100))}%",
            "detected_terms": detected_terms,
            "sla_hours": sla_hours,
            "category_breakdown": score_breakdown,
            "response_time_ms": elapsed_ms
        }

        if save_log:
            try:
                log_entry = AnalysisLog(
                    raw_text=text,
                    category=category,
                    priority=priority,
                    assigned_team=assigned_team,
                    confidence=confidence,
                    detected_terms=detected_terms,
                    response_time_ms=elapsed_ms
                )
                db.session.add(log_entry)
                db.session.commit()
                result["log_id"] = log_entry.id
            except Exception:
                db.session.rollback()

        return result
