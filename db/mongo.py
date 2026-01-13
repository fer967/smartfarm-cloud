import pprint

def save_reading(data):
    """Stub implementation: in real project this would save to MongoDB."""
    pprint.pprint({"action": "save_reading", "data": data})

def save_alert(alert):
    """Stub implementation: in real project this would save alerts to MongoDB."""
    pprint.pprint({"action": "save_alert", "alert": alert})
