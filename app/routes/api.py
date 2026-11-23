from flask import Blueprint, request, jsonify
from app.services.analyzer_service import AnalyzerService
from app.models.ticket import Ticket, AnalysisLog
from app.utils.extensions import db

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

@api_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "AI IT Helpdesk Analyzer",
        "version": "1.0.0"
    }), 200

@api_bp.route("/analyze", methods=["POST"])
def analyze_endpoint():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "") or data.get("description", "") or data.get("query", "")

    if not text:
        return jsonify({
            "error": "Missing required field 'text'",
            "example": {"text": "My laptop is not connecting to the office Wi-Fi"}
        }), 400

    save_log = data.get("save_log", True)
    analysis = AnalyzerService.analyze_ticket(text, save_log=save_log)
    return jsonify(analysis), 200

@api_bp.route("/tickets", methods=["GET"])
def list_tickets():
    query = Ticket.query

    category = request.args.get("category")
    priority = request.args.get("priority")
    team = request.args.get("team")
    status = request.args.get("status")

    if category:
        query = query.filter_by(category=category)
    if priority:
        query = query.filter_by(priority=priority)
    if team:
        query = query.filter_by(assigned_team=team)
    if status:
        query = query.filter_by(status=status)

    tickets = query.order_by(Ticket.created_at.desc()).all()
    return jsonify({
        "total": len(tickets),
        "tickets": [t.to_dict() for t in tickets]
    }), 200

@api_bp.route("/tickets", methods=["POST"])
def create_ticket():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()

    if not title or not description:
        return jsonify({"error": "Both 'title' and 'description' are required."}), 400

    full_context = f"{title}. {description}"
    analysis = AnalyzerService.analyze_ticket(full_context, save_log=False)

    ticket = Ticket(
        title=title,
        description=description,
        category=analysis["category"],
        priority=analysis["priority"],
        assigned_team=analysis["assigned_team"],
        confidence=analysis["confidence"],
        detected_terms=analysis["detected_terms"],
        sla_hours=analysis["sla_hours"],
        status="Open"
    )

    db.session.add(ticket)
    db.session.commit()

    return jsonify({
        "message": "Ticket created and auto-classified successfully",
        "ticket": ticket.to_dict(),
        "analysis": analysis
    }), 201

@api_bp.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return jsonify(ticket.to_dict()), 200

@api_bp.route("/stats", methods=["GET"])
def get_stats():
    total_tickets = Ticket.query.count()
    total_logs = AnalysisLog.query.count()

    categories = db.session.query(Ticket.category, db.func.count(Ticket.id)).group_by(Ticket.category).all()
    priorities = db.session.query(Ticket.priority, db.func.count(Ticket.id)).group_by(Ticket.priority).all()
    teams = db.session.query(Ticket.assigned_team, db.func.count(Ticket.id)).group_by(Ticket.assigned_team).all()

    return jsonify({
        "total_tickets": total_tickets,
        "total_analyzed_requests": total_logs,
        "category_distribution": dict(categories),
        "priority_distribution": dict(priorities),
        "team_workload": dict(teams)
    }), 200
