"""Prices as the app prints them."""


def price_value(text: str) -> float:
    """'$ 29.99' -> 29.99"""
    return float(text.replace("$", "").replace(",", "").strip())
