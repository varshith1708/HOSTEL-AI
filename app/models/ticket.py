from datetime import datetime, timezone
import json
from app.utils.extensions import db

class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(50), nullable=False, default="Medium")
    assigned_team = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False, default=0.0)
    detected_terms_json = db.Column(db.Text, nullable=True, default="[]")
    status = db.Column(db.String(50), nullable=False, default="Open")
    sla_hours = db.Column(db.Float, nullable=False, default=8.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    resolved_at = db.Column(db.DateTime, nullable=True)

    @property
    def detected_terms(self):
        try:
            return json.loads(self.detected_terms_json or "[]")
        except Exception:
            return []

    @detected_terms.setter
    def detected_terms(self, terms_list):
        self.detected_terms_json = json.dumps(terms_list or [])

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "assigned_team": self.assigned_team,
            "confidence": round(self.confidence, 4),
            "confidence_pct": f"{round(self.confidence * 100, 1)}%",
            "detected_terms": self.detected_terms,
            "status": self.status,
            "sla_hours": self.sla_hours,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
        }


class AnalysisLog(db.Model):
    __tablename__ = "analysis_logs"

    id = db.Column(db.Integer, primary_key=True)
    raw_text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    assigned_team = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    detected_terms_json = db.Column(db.Text, nullable=True, default="[]")
    response_time_ms = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def detected_terms(self):
        try:
            return json.loads(self.detected_terms_json or "[]")
        except Exception:
            return []

    @detected_terms.setter
    def detected_terms(self, terms_list):
        self.detected_terms_json = json.dumps(terms_list or [])

    def to_dict(self):
        return {
            "id": self.id,
            "raw_text": self.raw_text,
            "category": self.category,
            "priority": self.priority,
            "assigned_team": self.assigned_team,
            "confidence": round(self.confidence, 4),
            "confidence_pct": f"{round(self.confidence * 100, 1)}%",
            "detected_terms": self.detected_terms,
            "response_time_ms": self.response_time_ms,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
