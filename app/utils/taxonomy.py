"""
IT Helpdesk Taxonomy, Routing Rules, and Knowledge Base definitions.
"""

CATEGORIES = {
    "Network Issue": {
        "keywords": [
            "wi-fi", "wifi", "ethernet", "vpn", "connecting", "connection", "connect",
            "dns", "gateway", "ip address", "packet loss", "latency", "router", "switch",
            "broadband", "internet", "lan", "wlan", "ssid", "firewall", "hotspot",
            "dhcp", "bandwidth", "signal", "disconnection", "office wi-fi"
        ],
        "default_team": "IT Network Team",
        "description": "Local area network, Wi-Fi, VPN connectivity, and network infrastructure issues."
    },
    "Infrastructure Issue": {
        "keywords": [
            "database", "production database", "prod db", "server", "cluster", "kubernetes",
            "k8s", "aws", "azure", "gcp", "redis", "postgres", "postgresql", "mysql",
            "down", "outage", "host", "datacenter", "storage", "san", "nas", "virtual machine",
            "vm", "ec2", "rds", "container", "docker", "pipeline", "cpu spike", "disk full"
        ],
        "default_team": "IT Infrastructure",
        "description": "Core servers, production databases, cloud services, and storage systems."
    },
    "Hardware Issue": {
        "keywords": [
            "laptop", "desktop", "monitor", "screen", "keyboard", "battery", "charger",
            "power adapter", "docking station", "headset", "mouse", "printer", "scanner",
            "motherboard", "ram", "memory", "overheating", "fan noise", "cracked", "usb"
        ],
        "default_team": "Hardware Support",
        "description": "Physical workstations, computer peripherals, and mobile devices."
    },
    "Software & Applications": {
        "keywords": [
            "crash", "bug", "slack", "teams", "outlook", "excel", "word", "powerpoint",
            "browser", "chrome", "firefox", "edge", "software update", "installation",
            "license", "git", "github", "ide", "vscode", "pycharm", "freezing"
        ],
        "default_team": "Application Support",
        "description": "Desktop apps, productivity suites, development tools, and software crashes."
    },
    "Security Incident": {
        "keywords": [
            "phishing", "malware", "ransomware", "unauthorized", "compromised", "breach",
            "virus", "suspicious email", "mfa bypass", "credential leak", "ddos", "trojan",
            "suspicious activity", "data leak", "hacked", "security alert"
        ],
        "default_team": "Security Operations Center (SOC)",
        "description": "Cybersecurity threats, phishing reports, malware, and compromised credentials."
    },
    "Access & Identity": {
        "keywords": [
            "password reset", "password expired", "account locked", "sso", "okta",
            "active directory", "permission denied", "mfa", "2fa", "login failed",
            "access request", "user role", "ldap", "unlock account"
        ],
        "default_team": "Identity & Access Management (IAM)",
        "description": "User accounts, password unlocks, single sign-on, and directory permissions."
    }
}

PRIORITY_LEVELS = {
    "Critical": {
        "sla_hours": 0.25,  # 15 minutes
        "color": "danger",
        "description": "Complete service outage affecting production, databases, or enterprise security."
    },
    "High": {
        "sla_hours": 2.0,
        "color": "warning",
        "description": "Major disruption impacting multiple teams, core applications, or high-urgency workflows."
    },
    "Medium": {
        "sla_hours": 8.0,
        "color": "primary",
        "description": "Single user workflow disruption, standard workstation network or device issues."
    },
    "Low": {
        "sla_hours": 24.0,
        "color": "secondary",
        "description": "General questions, routine peripheral requests, and non-blocking minor bugs."
    }
}

CRITICAL_TRIGGERS = [
    "production database", "prod database", "database is down", "prod is down",
    "production is down", "system outage", "datacenter down", "ransomware",
    "security breach", "all users affected", "payment gateway down"
]

HIGH_TRIGGERS = [
    "vpn down", "multiple users", "entire floor", "cannot process orders",
    "service degraded", "core service", "deployment failed", "data corruption"
]
