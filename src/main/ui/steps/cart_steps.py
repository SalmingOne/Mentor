import allure

from src.main.ui.pages.cart_page import CartPage


class CartSteps:
    def __init__(self, page):
        self.page = page
        self.cart_page = CartPage(page)

    @allure.step('Открыть страницу корзины')
    def open_by_link(self):
        self.cart_page.open()
        return self

    @allure.step('Открыть страницу корзины из каталога')
    def open_from_catalog(self):
        self.cart_page.open_from_catalog_page()
        return self

    @allure.step('Получить итоговую стоимость корзины')
    def get_products_total_price(self):
        return self.cart_page.get_item_total_price()

    @allure.step('Перейти к оплате')
    def checkout(self):
        self.cart_page.checkout()
        return self

    @allure.step('Удалить продукт из корзины {product_name}')
    def remove(self, product_name):
        self.cart_page.remove_item(product_name)

    @allure.step('Проверить, что продукт {product_name} в корзине')
    def check_product_in_cart(self, product_name):
        self.cart_page.expect_item_in_cart(product_name)
        return self

    @allure.step('Проверить, что продукта {product_name} нет в корзине')
    def check_product_not_in_cart(self, product_name):
        self.cart_page.expect_item_not_in_cart(product_name)
        return self