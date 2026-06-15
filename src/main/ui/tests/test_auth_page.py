from src.main.ui.pages.auth_page import AuthPage
from playwright.sync_api import expect, Page

from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.auth_steps import AuthSteps
from src.main.ui.steps.catalog_steps import CatalogSteps


class TestAuthPage:

    def test_auth(self, page):
        auth_steps = AuthSteps(page)
        auth_steps.open_auth_page()
        auth_steps.authenticate(username='standard_user',
                                password='secret_sauce')
        expect(page).to_have_url('https://www.saucedemo.com/inventory.html')

    def test_auth_locked(self, page: Page):
        auth_steps = AuthSteps(page)
        auth_steps.open_auth_page()
        auth_steps.authenticate(
            username='locked_out_user',
            password='secret_sauce'
        )
        assert 'Epic sadface: Sorry, this user has been locked out.' == auth_steps.get_error_text()

    def test_logout(self, auth_page: Page):
        catalog_steps = CatalogSteps(auth_page)
        catalog_steps.logout()

        expect(auth_page).to_have_url('https://www.saucedemo.com/')
