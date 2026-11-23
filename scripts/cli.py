import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.analyzer_service import AnalyzerService

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.cli \"<ticket description>\"")
        print("Example: python -m scripts.cli \"My laptop is not connecting to the office Wi-Fi\"")
        sys.exit(1)

    text = " ".join(sys.argv[1:])
    result = AnalyzerService.analyze_ticket(text, save_log=False)

    print("\n" + "=" * 60)
    print("AI IT Helpdesk Analyzer - Triage Summary")
    print("=" * 60)
    print(f"Input Text:       {result['input_text']}")
    print(f"Category:         {result['category']}")
    print(f"Priority:         {result['priority']} (SLA: {result['sla_hours']}h)")
    print(f"Assigned Team:    {result['assigned_team']}")
    print(f"Confidence:       {result['confidence_pct']} ({result['confidence']})")
    print(f"Detected Terms:   {', '.join(result['detected_terms']) if result['detected_terms'] else 'None'}")
    print(f"Response Time:    {result['response_time_ms']} ms")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
