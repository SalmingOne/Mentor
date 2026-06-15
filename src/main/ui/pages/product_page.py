from playwright.sync_api import Page


class ProductPage:

    def __init__(self, page: Page):
        self.page = page
        self.product_name = page.get_by_test_id('inventory-item-name')
        self.product_description = page.get_by_test_id('inventory-item-desc')
        self.product_price = page.get_by_test_id('inventory-item-price')


    def get_item_details(self):
        return self.product_name.inner_text(), self.product_description.inner_text(), self.product_price.inner_text()