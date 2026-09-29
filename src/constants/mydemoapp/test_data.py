"""Invented, non-personal test data (mobile-test-data: data built into the app, nothing to seed)."""

ADDRESS = {
    "full_name": "Test Buyer",
    "address_1": "1 Test Street",
    "city": "Testville",
    "zip": "12345",
    "country": "Testland",
}

CARD = {
    "name": "Test Buyer",
    "number": "4111111111111111",  # a standard test card number, never a real card
    "expiry": "0330",
    "security_code": "123",
}

LOCKED_OUT_USERNAME = "alice@example.com"
UNKNOWN_USERNAME = "nobody@example.com"
WRONG_PASSWORD = "wrong-password"


def price_value(text: str) -> float:
    """'$ 29.99' -> 29.99"""
    return float(text.replace("$", "").replace(",", "").strip())
