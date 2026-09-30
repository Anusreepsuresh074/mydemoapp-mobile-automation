"""Invented, non-personal checkout data (the app needs nothing seeded)."""

import pytest

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

REQUIRED_ADDRESS_ERRORS = {
    "full_name": "Please provide your full name.",
    "address_1": "Please provide your address.",
    "city": "Please provide your city.",
    "zip": "Please provide your zip",
    "country": "Please provide your country.",  # the app shows "Please provide your" (D-05)
}

MISSING_ADDRESS_FIELD = [pytest.param(field, id=field) for field in REQUIRED_ADDRESS_ERRORS]

PAYMENT_ERROR = "Value looks invalid."

DELIVERY = ("DHL Standard Delivery", "$5.99")
