"""Sign-in test data. The demo account itself comes from the environment (test_user fixture)."""

LOCKED_OUT_USERNAME = "alice@example.com"
UNKNOWN_USERNAME = "nobody@example.com"
WRONG_PASSWORD = "wrong-password"
NOT_AN_EMAIL = "bob"
LONG_USERNAME = "a" * 288 + "@example.com"  # 300 characters
SPECIAL_CHARACTERS_USERNAME = "<script>'\";--@x.com"
LISTED_DEMO_USERNAME = "bod@example.com"  # spelled this way by the app's own login screen
LOGOUT_QUESTION = "Are you sure you want to logout"
