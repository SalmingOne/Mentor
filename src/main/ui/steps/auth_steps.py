import allure

from src.main.ui.pages.auth_page import AuthPage


class AuthSteps:

    def __init__(self, page):
        self.page = page
        self.auth_page = AuthPage(page)

    @allure.step('Открыть страницу авторизации')
    def open_auth_page(self):
        self.auth_page.open()
        return self
    @allure.step('Авторизоваться под пользователем {username}')
    def authenticate(self, username, password):
        self.auth_page.login(username, password)
        return self

    @allure.step('Получить текст ошибки')
    def get_error_text(self):
        return self.auth_page.get_error_text()