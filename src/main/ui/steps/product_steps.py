import allure

from src.main.ui.pages.product_page import ProductPage


class ProductSteps:
    def __init__(self, page):
        self.page = page
        self.product_page = ProductPage(page)

    @allure.step('Получить детали продукте')
    def get_product_details(self):
        return self.product_page.get_item_details()