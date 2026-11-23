from app.services.keyword_service import KeywordService
from app.services.priority_service import PriorityService
from app.services.routing_service import RoutingService
from app.services.classification_service import ClassificationService

def test_keyword_extraction():
    text = "My laptop is not connecting to the office Wi-Fi"
    terms = KeywordService.extract_detected_terms(text)
    lower_terms = [t.lower() for t in terms]

    assert "wi-fi" in lower_terms
    assert "connecting" in lower_terms
    assert "laptop" in lower_terms

def test_priority_service_critical_triggers():
    priority, sla = PriorityService.evaluate_priority("production database is down", "Infrastructure Issue", ["production database", "down"])
    assert priority == "Critical"
    assert sla == 0.25

def test_priority_service_medium_default():
    priority, sla = PriorityService.evaluate_priority("laptop cannot connect to wifi", "Network Issue", ["laptop", "wifi"])
    assert priority == "Medium"
    assert sla == 8.0

def test_routing_service():
    team = RoutingService.determine_team("Network Issue", "Medium", ["wi-fi", "connecting"])
    assert team == "IT Network Team"

    team_infra = RoutingService.determine_team("Infrastructure Issue", "Critical", ["production database", "down"], "production database is down")
    assert team_infra == "IT Infrastructure"

def test_classification_service():
    category, conf, _ = ClassificationService.classify("Cannot connect to office Wi-Fi", ["wi-fi", "connecting"])
    assert category == "Network Issue"
    assert conf > 0.85
