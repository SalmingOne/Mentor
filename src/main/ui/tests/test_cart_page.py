import random

import pytest
from playwright.sync_api import Page, expect
from pytest_check import equal

from src.main.ui.pages.cart_page import CartPage
from src.main.ui.pages.checkout_page import CheckoutPage
from mimesis import Person

from src.main.ui.steps.cart_steps import CartSteps
from src.main.ui.steps.checkout_steps import CheckoutSteps

person = Person(locale='en')


class TestCartPage:

    def test_open_cart_page(self, auth_page: Page):
        cart_steps = CartSteps(auth_page)
        cart_steps.open_from_catalog()

        expect(auth_page).to_have_url('https://www.saucedemo.com/cart.html')


    @pytest.mark.parametrize('add_items_to_cart', [1,3], indirect=True, ids=['one_item', 'many_items'])
    def test_checkout_items(self, auth_page: Page, add_items_to_cart):
        cart_steps = CartSteps(auth_page)
        checkout_steps = CheckoutSteps(auth_page)

        cart_steps.open_by_link()
        total_price = cart_steps.get_products_total_price()
        cart_steps.checkout()

        checkout_steps.start_checkout(person.first_name(), person.last_name(), random.randint(1, 100))
        checkout_price = checkout_steps.get_products_total_price()
        equal(total_price, checkout_price)
        checkout_steps.finish_checkout()
        checkout_steps.check_complete_checkout()

    @pytest.mark.parametrize('add_items_to_cart', [3], indirect=True)
    def test_remove_cart_item(self, auth_page: Page, add_items_to_cart):

        cart_steps = CartSteps(auth_page)
        cart_steps.open_by_link()
        item_to_remove = random.choice(add_items_to_cart)
        cart_steps.check_product_in_cart(item_to_remove)
        cart_steps.remove(item_to_remove)
        cart_steps.check_product_not_in_cart(item_to_remove)

