import allure
import pytest

from src.pages.login_page import LoginPage
from tests.login.login_td import (
    LISTED_DEMO_USERNAME,
    LOCKED_OUT_USERNAME,
    LOGOUT_QUESTION,
    LONG_USERNAME,
    NOT_AN_EMAIL,
    SPECIAL_CHARACTERS_USERNAME,
    UNKNOWN_USERNAME,
    WRONG_PASSWORD,
)

pytestmark = allure.feature("Sign-in")


@pytest.fixture
def login_page(catalog) -> LoginPage:
    page = catalog.header.open_menu().choose_log_in()
    assert page.is_open()
    return page


def _is_signed_in(catalog, login_page) -> bool:
    """Signed in = the side menu offers Log Out (the menu button is on the login screen too)."""
    return catalog.header.open_menu().shows_log_out()


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.p0
@allure.title("LGN-P0-01 The demo user can sign in")
def test_demo_user_can_sign_in(catalog, login_page, test_user):
    login_page.log_in(*test_user)
    assert _is_signed_in(catalog, login_page), "menu does not offer Log Out after signing in"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("LGN-P1-02 Empty username is refused")
def test_empty_username_is_refused(login_page):
    login_page.log_in("", "")
    assert login_page.username_error() == "Username is required"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("LGN-P1-03 Missing password is refused")
def test_missing_password_is_refused(login_page, test_user):
    login_page.log_in(test_user[0], "")
    assert login_page.password_error() == "Enter Password"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("LGN-P1-04 The locked-out user is refused")
def test_locked_out_user_is_refused(login_page, test_user):
    login_page.log_in(LOCKED_OUT_USERNAME, test_user[1])
    assert login_page.password_error() == "Sorry this user has been locked out."
    assert login_page.is_open()


@pytest.mark.regression
@pytest.mark.p1
@pytest.mark.xfail(reason="D-01: any username and password are accepted", strict=True)
@allure.title("LGN-P1-05 An unknown user is refused (known defect D-01)")
def test_unknown_user_is_refused(catalog, login_page):
    login_page.log_in(UNKNOWN_USERNAME, WRONG_PASSWORD)
    assert not _is_signed_in(catalog, login_page), "unknown credentials were accepted"


@pytest.mark.regression
@pytest.mark.p1
@pytest.mark.xfail(reason="D-01: a wrong password is accepted for the real user", strict=True)
@allure.title("LGN-P1-06 The real user with a wrong password is refused (known defect D-01)")
def test_wrong_password_is_refused(catalog, login_page, test_user):
    login_page.log_in(test_user[0], WRONG_PASSWORD)
    assert not _is_signed_in(catalog, login_page), "a wrong password was accepted"


@pytest.mark.regression
@pytest.mark.p2
@pytest.mark.xfail(reason="D-04: any text is accepted as a username", strict=True)
@allure.title("LGN-P2-07 A username that is not an email is refused (known defect D-04)")
def test_username_that_is_not_an_email_is_refused(catalog, login_page, test_user):
    login_page.log_in(NOT_AN_EMAIL, test_user[1])
    assert not _is_signed_in(catalog, login_page), "a username that is not an email was accepted"


def _app_survives(catalog, login_page) -> bool:
    return login_page.app_is_in_foreground() and (login_page.is_open() or catalog.is_open())


@pytest.mark.regression
@pytest.mark.p2
@allure.title("LGN-P2-08 A 300-character username does not crash the app")
def test_long_username_does_not_crash(catalog, login_page, test_user):
    login_page.log_in(LONG_USERNAME, test_user[1])
    assert _app_survives(catalog, login_page), "the app closed or shows no screen"


@pytest.mark.regression
@pytest.mark.p2
@allure.title("LGN-P2-09 Special characters in the username do not crash the app")
def test_special_characters_username_does_not_crash(catalog, login_page, test_user):
    login_page.log_in(SPECIAL_CHARACTERS_USERNAME, test_user[1])
    assert _app_survives(catalog, login_page), "the app closed or shows no screen"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("LGN-P1-10 The password is hidden while typing")
def test_password_is_masked(login_page):
    assert login_page.password_is_masked()


@pytest.mark.regression
@pytest.mark.p1
@allure.title("LGN-P1-11 Tapping a demo username fills the form")
def test_tapping_a_demo_username_fills_the_form(catalog, login_page):
    assert login_page.demo_username() == LISTED_DEMO_USERNAME
    login_page.use_demo_user()
    assert login_page.typed_username() == LISTED_DEMO_USERNAME
    assert login_page.password_is_filled()
    login_page.submit()
    assert _is_signed_in(catalog, login_page)


@pytest.mark.regression
@pytest.mark.p1
@allure.title("LGN-P1-12 Cancelling Log Out keeps you signed in")
def test_cancelling_log_out_keeps_you_signed_in(signed_in):
    menu = signed_in.header.open_menu()
    assert menu.choose_log_out() == LOGOUT_QUESTION
    menu.cancel_log_out()
    if not menu.shows_log_out():
        menu = signed_in.header.open_menu()
    assert menu.shows_log_out(), "signed out although Log Out was cancelled"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("LGN-P1-13 Log Out signs you out")
def test_log_out_signs_you_out(app, signed_in):
    menu = signed_in.header.open_menu()
    assert menu.choose_log_out() == LOGOUT_QUESTION
    menu.confirm_log_out()
    assert LoginPage(app).is_open(), "Login did not open after logging out"
    assert signed_in.header.open_menu().shows_log_in()
