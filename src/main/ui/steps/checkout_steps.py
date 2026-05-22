import allure
from playwright.sync_api import Page

from src.main.ui.pages.checkout_page import CheckoutPage


class CheckoutSteps:

    def __init__(self, page: Page):
        self.page = page
        self.checkout_page = CheckoutPage(page)

    @allure.step('Начать процесс формирования заказа')
    def start_checkout(self, first_name: str, last_name: str, postal_code: int):
        self.checkout_page.start_checkout(first_name, last_name, postal_code)
        return self

    @allure.step('Получить итоговую стоимость заказа')
    def get_products_total_price(self):
        return self.checkout_page.get_total_price()

    @allure.step('Завершить оплату')
    def finish_checkout(self):
        self.checkout_page.finish_checkout()
        return self

    @allure.step('Проверить завершение транзакции')
    def check_complete_checkout(self):
        self.checkout_page.expect_complete_container_is_displayed()
        return self