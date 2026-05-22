from playwright.sync_api import Page


class AuthPage:
    URL = 'https://www.saucedemo.com/'
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_test_id('username')
        self.password_input = page.get_by_test_id('password')
        self.login_button = page.get_by_test_id('login-button')
        self.error_text = page.locator('.error-message-container')


    def __getattr__(self, name):
        return getattr(self.page, name)

    def open(self):
        self.page.goto(self.URL)


    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()


    def get_error_text(self):
        return self.error_text.inner_text()
