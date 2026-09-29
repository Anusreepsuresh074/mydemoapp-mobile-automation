from src.screens.mydemoapp.login_screen import LoginScreen


class LoginActions:
    def __init__(self, driver):
        self.screen = LoginScreen(driver)

    def is_open(self) -> bool:
        return self.screen.is_visible(LoginScreen.btn_login)

    def log_in(self, username: str, password: str) -> None:
        if username:
            self.screen.type_text(LoginScreen.input_username, username)
        if password:
            self.screen.type_text(LoginScreen.input_password, password)
        self.screen.tap(LoginScreen.btn_login)

    def username_error(self) -> str:
        return self.screen.text_of(LoginScreen.msg_username_error)

    def password_error(self) -> str:
        return self.screen.text_of(LoginScreen.msg_password_error)
