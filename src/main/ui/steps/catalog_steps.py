import allure
from playwright.sync_api import Page

from src.main.ui.pages.catalog_page import CatalogPage


class CatalogSteps:

    def __init__(self, page: Page):
        self.page = page
        self.catalog_page = CatalogPage(page)

    @allure.step('Выйти из системы')
    def logout(self):
        self.catalog_page.logout()
        return self

    @allure.step('Отсортировать продукты ({order})')
    def sort_items(self, order='az'):
        self.catalog_page.sorting(option=order)
        return self

    @allure.step('Получить названия продуктов')
    def get_product_names(self):
        return self.catalog_page.get_catalog_item_names()

    @allure.step('Получить цены продуктов')
    def get_product_prices(self):
        return self.catalog_page.get_catalog_item_prices()

    @allure.step('Добавить в корзину')
    def add_to_cart(self, product_name):
        return self.catalog_page.add_to_cart(product_name)

    @allure.step('Получить кол-во продуктов в корзине')
    def get_count_of_products_in_cart(self):
        return self.catalog_page.get_cart_count()

    @allure.step('Удалить продукт {product_name} из корзины со страницы каталога')
    def remove_from_cart(self, product_name):
        return self.catalog_page.remove_from_cart(product_name)

    @allure.step('Получить текст карточки продукта {product_name}')
    def get_product_card_text(self, product_name):
        return self.catalog_page.get_card_text(product_name)

    @allure.step('Открыть страницу продукта {product_name}')
    def open_product_details(self, product_name):
        self.catalog_page.open_item_details(product_name)
        return self