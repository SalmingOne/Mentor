from playwright.sync_api import Page, expect
from src.main.ui.testutils import _smart_type


class CartPage:
    URL = 'https://www.saucedemo.com/cart.html'

    def __init__(self, page: Page):
        self.page = page
        self.checkout_button = page.get_by_test_id('checkout')
        self.product_cards = page.get_by_test_id('inventory-item')
        self.shopping_cart = page.get_by_test_id('shopping-cart-link')

    def __getattr__(self, name):
        return getattr(self.page, name)

    def open(self):
        self.page.goto(self.URL, wait_until='networkidle')


    def open_from_catalog_page(self):
        self.shopping_cart.click()

    def remove_item(self, item_name: str):
        card = self.product_cards.filter(has_text=item_name)
        card.get_by_role("button").click()

    def get_cart_items_name(self):
        return [card.get_by_test_id('inventory-item-name') for card in self.product_cards.all()]

    def checkout(self):
        self.checkout_button.click()

    def get_item_total_price(self):
        total_price = 0
        for cart in self.product_cards.all():
            total_price += _smart_type(cart.get_by_test_id('inventory-item-price').inner_text())

        return round(total_price * 1.08, 2)

    def expect_item_in_cart(self, item_name: str):
        card = self.product_cards.filter(has_text=item_name)
        expect(card).to_be_visible()

    def expect_item_not_in_cart(self, item_name: str):
        card = self.product_cards.filter(has_text=item_name)
        expect(card).not_to_be_visible()
