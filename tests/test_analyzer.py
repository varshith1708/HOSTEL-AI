from app.services.analyzer_service import AnalyzerService

def test_wifi_laptop_incident_benchmark():
    """
    Test case specified by user requirement:
    'My laptop is not connecting to the office Wi-Fi' ->
    Network Issue, Medium priority, IT Network Team, ~94% confidence,
    with detected terms Wi-Fi / connecting / laptop.
    """
    text = "My laptop is not connecting to the office Wi-Fi"
    result = AnalyzerService.analyze_ticket(text, save_log=False)

    assert result["category"] == "Network Issue"
    assert result["priority"] == "Medium"
    assert result["assigned_team"] == "IT Network Team"
    assert result["confidence"] == 0.94
    assert result["confidence_pct"] == "~94%"

    # Verify detected terms include Wi-Fi, connecting, laptop
    detected_terms_lower = [t.lower() for t in result["detected_terms"]]
    assert "wi-fi" in detected_terms_lower
    assert "connecting" in detected_terms_lower
    assert "laptop" in detected_terms_lower


def test_production_database_down_benchmark():
    """
    Test case specified by user requirement:
    'production database is down' routes to IT Infrastructure at Critical priority.
    """
    text = "production database is down"
    result = AnalyzerService.analyze_ticket(text, save_log=False)

    assert result["category"] == "Infrastructure Issue"
    assert result["priority"] == "Critical"
    assert result["assigned_team"] == "IT Infrastructure"
    assert result["confidence"] >= 0.95

    detected_terms_lower = [t.lower() for t in result["detected_terms"]]
    assert "production database" in detected_terms_lower
    assert "down" in detected_terms_lower


def test_empty_input_handling():
    result = AnalyzerService.analyze_ticket("", save_log=False)
    assert "error" in result
    assert result["confidence"] == 0.0
