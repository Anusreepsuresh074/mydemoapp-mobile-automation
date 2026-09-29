"""Login."""

from src.core.base_screen import BaseScreen
from src.screens.mydemoapp._ids import rid


class LoginScreen(BaseScreen):
    txt_title = rid("loginTV")
    input_username = rid("nameET")
    input_password = rid("passwordET")
    btn_login = rid("loginBtn")
    msg_username_error = rid("nameErrorTV")
    msg_password_error = rid("passwordErrorTV")
