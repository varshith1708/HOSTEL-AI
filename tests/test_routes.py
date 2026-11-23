import json

def test_health_check(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"

def test_api_analyze(client):
    payload = {"text": "My laptop is not connecting to the office Wi-Fi"}
    res = client.post("/api/v1/analyze", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["category"] == "Network Issue"
    assert data["priority"] == "Medium"
    assert data["assigned_team"] == "IT Network Team"
    assert data["confidence"] == 0.94

def test_api_tickets_create_and_list(client):
    payload = {
        "title": "Outage alert",
        "description": "production database is down on us-east cluster"
    }
    res = client.post("/api/v1/tickets", json=payload)
    assert res.status_code == 201
    ticket = res.get_json()["ticket"]
    assert ticket["priority"] == "Critical"
    assert ticket["assigned_team"] == "IT Infrastructure"

    # List tickets
    list_res = client.get("/api/v1/tickets")
    assert list_res.status_code == 200
    data = list_res.get_json()
    assert data["total"] >= 1

def test_api_stats(client):
    res = client.get("/api/v1/stats")
    assert res.status_code == 200
    data = res.get_json()
    assert "total_tickets" in data

def test_index_page(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"AI IT Helpdesk" in res.data
