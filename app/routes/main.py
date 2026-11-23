from flask import Blueprint, render_template, request
from app.models.ticket import Ticket
from app.services.analyzer_service import AnalyzerService

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    analysis = None
    input_text = ""
    if request.method == "POST":
        input_text = request.form.get("ticket_text", "").strip()
        if input_text:
            analysis = AnalyzerService.analyze_ticket(input_text, save_log=True)

    recent_tickets = Ticket.query.order_by(Ticket.created_at.desc()).limit(5).all()
    return render_template("index.html", analysis=analysis, input_text=input_text, recent_tickets=recent_tickets)

@main_bp.route("/dashboard")
def dashboard():
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template("dashboard.html", tickets=tickets)
