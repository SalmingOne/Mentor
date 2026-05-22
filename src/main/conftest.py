from src.main.api.fixtures.api_fixture import *
from src.main.api.fixtures.admin_fixture import *
from src.main.api.fixtures.object_fixture import *
from src.main.api.fixtures.user_fixture import *
from src.main.api.fixtures.db_fixture import *
from src.main.ui.pages.auth_page import AuthPage
from src.main.ui.pages.catalog_page import CatalogPage
import random


# @pytest.fixture
# def playwright_instance():
#     with sync_playwright() as p:
#         yield p
#
#
# @pytest.fixture
# def browser(playwright_instance):
#     browser = playwright_instance.chromium.launch(headless=False)
#     yield browser
#     browser.close()
#
#
# @pytest.fixture(scope='function')
# def page(browser):
#     context = browser.new_context()
#     page = context.new_page()
#     yield page
#     context.close()

@pytest.fixture(scope='session', autouse=True)
def playwright_configure(playwright):
    playwright.selectors.set_test_id_attribute('data-test')

@pytest.fixture()
def auth_page(page):
    auth_page = AuthPage(page)
    auth_page.open()
    auth_page.login(
        username='standard_user',
        password='secret_sauce'
    )
    return page


@pytest.fixture()
def add_items_to_cart(auth_page, request):
    items_count = getattr(request, 'param', 1)

    catalog_page = CatalogPage(auth_page)
    items = random.sample(catalog_page.get_catalog_item_names(), k=items_count)
    for item in items:
        catalog_page.add_to_cart(item)

    yield items

    # удаление через API
