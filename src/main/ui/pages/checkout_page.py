from playwright.sync_api import Page, expect

from src.main.ui.testutils import _smart_type


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name_field = page.get_by_test_id('firstName')
        self.last_name_field = page.get_by_test_id('lastName')
        self.postal_code_field = page.get_by_test_id('postalCode')
        self.continue_button = page.get_by_test_id('continue')
        self.cancel_button = page.get_by_test_id('cancel')
        self.finish_button = page.get_by_test_id('finish')
        self.cards = page.get_by_test_id('inventory-item')
        self.total_price = page.get_by_test_id('total-label')
        self.complete_container = self.page.get_by_test_id('checkout-complete-container')


    def start_checkout(self, first_name: str, last_name: str, postal_code: int):
        self.first_name_field.fill(first_name)
        self.last_name_field.fill(last_name)
        self.postal_code_field.fill(str(postal_code))
        self.continue_button.click()


    def get_total_price(self):
        return _smart_type(self.total_price.inner_text())

    def finish_checkout(self):
        self.finish_button.click()

    def expect_complete_container_is_displayed(self):
        expect(self.complete_container).to_be_visible()
