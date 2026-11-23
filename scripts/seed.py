import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.utils.extensions import db
from app.models.ticket import Ticket
from app.services.analyzer_service import AnalyzerService

SAMPLE_INCIDENTS = [
    {
        "title": "Office Wi-Fi disconnection on laptop",
        "description": "My laptop is not connecting to the office Wi-Fi",
    },
    {
        "title": "Core production outage",
        "description": "production database is down",
    },
    {
        "title": "VPN gateway failure",
        "description": "Corporate VPN down for entire remote engineering team",
    },
    {
        "title": "Account locked out",
        "description": "Active Directory account locked after password expired",
    },
    {
        "title": "Phishing detection",
        "description": "Received suspicious phishing email with external credential harvest link",
    },
    {
        "title": "Hardware peripheral replacement",
        "description": "Requesting a replacement wireless mouse and keyboard",
    }
]

def seed_database():
    app = create_app()
    with app.app_context():
        print("Initializing database tables...")
        db.create_all()

        existing_count = Ticket.query.count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} tickets. Skipping seed.")
            return

        print("Seeding sample incident tickets...")
        for item in SAMPLE_INCIDENTS:
            full_text = f"{item['title']}. {item['description']}"
            analysis = AnalyzerService.analyze_ticket(full_text, save_log=False)

            ticket = Ticket(
                title=item["title"],
                description=item["description"],
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
        print(f"Successfully seeded {len(SAMPLE_INCIDENTS)} IT Helpdesk tickets.")

if __name__ == "__main__":
    seed_database()
