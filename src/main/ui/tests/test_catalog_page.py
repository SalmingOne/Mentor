import random

from playwright.sync_api import Page
from playwright.sync_api import expect

from src.main.ui.pages.catalog_page import CatalogPage
from pytest_check import equal

from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.product_steps import ProductSteps
from src.main.ui.testutils import sorted_dict_by_value


class TestCatalogPage:

    def test_sorting_by_name(self, auth_page: Page):
        catalog_steps = CatalogSteps(auth_page)
        items = catalog_steps.get_product_names()
        catalog_steps.sort_items()
        equal(catalog_steps.get_product_names(), sorted(items))
        catalog_steps.sort_items('za')
        equal(catalog_steps.get_product_names(), sorted(items, reverse=True))


    def test_sorting_by_price(self, auth_page: Page):
        catalog_steps = CatalogSteps(auth_page)
        items = catalog_steps.get_product_prices()
        catalog_steps.sort_items('lohi')
        equal(catalog_steps.get_product_names(), list(sorted_dict_by_value(items).keys()))
        catalog_steps.sort_items('hilo')
        equal(catalog_steps.get_product_names(), list(sorted_dict_by_value(items, reverse=True).keys()))

    def test_add_to_cart(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        item = random.choice(catalog_steps.get_product_names())
        button = catalog_steps.add_to_cart(item)

        expect(button).to_have_text('Remove')
        equal(catalog_steps.get_count_of_products_in_cart(), 1)


    def test_add_and_delete_from_cart(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        item = random.choice(catalog_steps.get_product_names())
        catalog_steps.add_to_cart(item)
        equal(catalog_steps.get_count_of_products_in_cart(), 1)
        button = catalog_steps.remove_from_cart(item)

        expect(button).to_have_text('Add to cart')
        equal(catalog_steps.get_count_of_products_in_cart(), 0)

    def test_item_details(self, auth_page: Page):
        catalog_steps = CatalogSteps(auth_page)
        product_steps = ProductSteps(auth_page)
        item = random.choice(catalog_steps.get_product_names())
        name, description, price = catalog_steps.get_product_card_text(item)
        catalog_steps.open_product_details(item)

        detail_name, detail_description, detail_price = product_steps.get_product_details()

        equal(name, detail_name)
        equal(description, detail_description)
        equal(price, detail_price)


