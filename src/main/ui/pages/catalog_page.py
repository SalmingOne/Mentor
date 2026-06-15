from playwright.sync_api import Page

class CatalogPage:

    def __init__(self, page: Page):
        self.page = page
        self.menu_button = page.locator('#react-burger-menu-btn')
        self.logout_button = page.get_by_test_id('logout-sidebar-link')
        self.sorting_select = page.get_by_test_id('product-sort-container')
        self.product_cards = page.get_by_test_id('inventory-item')
        self.things_count = page.get_by_test_id('shopping-cart-badge')

    def __getattr__(self, name):
        return getattr(self.page, name)

    def logout(self):
        self.menu_button.click()
        self.logout_button.click()

    def sorting(self, option='az'):
        self.sorting_select.select_option(option)

    def get_catalog_item_names(self):
        return self.product_cards.get_by_test_id('inventory-item-name').all_text_contents()

    def get_catalog_item_prices(self):
        return dict(zip(self.get_catalog_item_names(), self.product_cards.get_by_test_id('inventory-item-price').all_text_contents()))

    def add_to_cart(self, item_name: str):
        card = self.product_cards.filter(has_text=item_name)
        button = card.get_by_role('button')
        if button.inner_text() == 'Add to cart':
            button.click()
        return button

    def remove_from_cart(self, item_name: str):
        card = self.product_cards.filter(has_text=item_name)
        button = card.get_by_role('button')
        if button.inner_text() == 'Remove':
            button.click()
        return button

    def get_cart_count(self):
        if self.things_count.is_hidden():
            return 0
        return int(self.things_count.inner_text())

    def get_card_text(self, item_name: str):
        card = self.product_cards.filter(has_text=item_name)
        name = card.get_by_test_id('inventory-item-name').inner_text()
        description = card.get_by_test_id('inventory-item-desc').inner_text()
        price = card.get_by_test_id('inventory-item-price').inner_text()

        return name, description, price


    def open_item_details(self, item_name: str):
        card = self.product_cards.filter(has_text=item_name)
        card.get_by_test_id('inventory-item-name').click()




