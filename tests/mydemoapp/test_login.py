import allure
import pytest

from src.actions.mydemoapp.login_actions import LoginActions
from src.actions.mydemoapp.menu_actions import MenuActions
from src.constants.mydemoapp.test_data import LOCKED_OUT_USERNAME, UNKNOWN_USERNAME, WRONG_PASSWORD
from src.core.config import credentials
from src.flows.mydemoapp.shopping_flows import sign_in_from_menu

pytestmark = allure.feature("Sign-in")


def _open_login(driver) -> LoginActions:
    menu = MenuActions(driver)
    menu.open()
    menu.choose_log_in()
    login = LoginActions(driver)
    assert login.is_open()
    return login


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.p0
@allure.title("LGN-P0-01 The demo user can sign in")
def test_demo_user_can_sign_in(app):
    username, password = credentials()
    sign_in_from_menu(app, username, password)
    menu = MenuActions(app)
    menu.open()
    assert menu.shows_log_out(), "menu does not offer Log Out after signing in"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("LGN-P1-02 Empty username is refused")
def test_empty_username_is_refused(app):
    login = _open_login(app)
    login.log_in("", "")
    assert login.username_error() == "Username is required"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("LGN-P1-03 Missing password is refused")
def test_missing_password_is_refused(app):
    username, _ = credentials()
    login = _open_login(app)
    login.log_in(username, "")
    assert login.password_error() == "Enter Password"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("LGN-P1-04 The locked-out user is refused")
def test_locked_out_user_is_refused(app):
    _, password = credentials()
    login = _open_login(app)
    login.log_in(LOCKED_OUT_USERNAME, password)
    assert login.password_error() == "Sorry this user has been locked out."
    assert login.is_open()


@pytest.mark.regression
@pytest.mark.p1
@pytest.mark.xfail(reason="Known defect: any username and password are accepted", strict=True)
@allure.title("LGN-P1-05 Wrong credentials are refused (known defect)")
def test_wrong_credentials_are_refused(app):
    login = _open_login(app)
    login.log_in(UNKNOWN_USERNAME, WRONG_PASSWORD)
    menu = MenuActions(app)
    if not login.is_open():
        menu.open()
    assert login.is_open() and not menu.shows_log_out(), "unknown credentials were accepted"
