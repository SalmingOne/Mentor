import time
from time import sleep

from playwright.sync_api import sync_playwright, expect
from pytest_check import equal


def test_textbox():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://demoqa.com/text-box')
        page.fill("#userName", 'test data')
        page.fill("#userEmail", 'test@mail.com')
        page.fill("#currentAddress", 'Moscow')
        page.fill("#permanentAddress", 'New York')
        page.get_by_role('button', name='Submit').click()
        text = page.text_content('#output')
        assert f"Name:test dataEmail:test@mail.comCurrent Address :Moscow Permananet Address :New York" == text


def test_checkbox(page):
    page.goto('https://demoqa.com/checkbox')
    while True:
        switchers = page.locator('.rc-tree-switcher.rc-tree-switcher_close')
        if switchers.count() == 0:
            break
        switchers.first.click()

    checkboxes = page.get_by_role('checkbox')
    for checkbox in checkboxes.all():
        checkbox.check()

    assert page.locator('#result').inner_text() == ('You have selected :\n'
                                                    'home\n'
                                                    'desktop\n'
                                                    'documents\n'
                                                    'downloads\n'
                                                    'notes\n'
                                                    'commands\n'
                                                    'workspace\n'
                                                    'office\n'
                                                    'wordFile\n'
                                                    'excelFile\n'
                                                    'react\n'
                                                    'angular\n'
                                                    'veu\n'
                                                    'public\n'
                                                    'private\n'
                                                    'classified\n'
                                                    'general')


def test_radiobutton(page):
    page.goto('https://demoqa.com/radio-button')
    containers = page.locator('.col-auto.form-check').all()
    for container in containers:
        radio_button = container.locator('input[type="radio"]')
        label = container.locator('.form-check-label')
        if not radio_button.is_disabled():
            radio_button.click()
            expect(radio_button).to_be_checked()
            expect(page.locator('.text-success')).to_have_text(label.inner_text())


def test_buttons(page):
    page.goto('https://demoqa.com/buttons')

    page.dblclick('#doubleClickBtn')
    assert ['You have done a double click'] == [p.text_content() for p in page.get_by_role('paragraph').all()]

    page.click('#rightClickBtn', button='right')
    assert ['You have done a double click', 'You have done a right click'] == [p.text_content() for p in page.get_by_role(
                                                                                   'paragraph').all()]

    page.get_by_role("button", name="Click Me", exact=True).click()
    assert ['You have done a double click', 'You have done a right click', 'You have done a dynamic click'] == [p.text_content()
                                                                                                                for p in
                                                                                                                page.get_by_role(
                                                                                                                    'paragraph').all()]

def test_upload_file(page, tmp_path):
    page.goto('https://demoqa.com/upload-download')

    file_path = tmp_path / 'test_file.txt'
    file_path.write_text('Random String')

    file_path_2 = tmp_path / 'test_file_1.txt'
    file_path_2.write_text('123')

    page.set_input_files('#uploadFile', file_path)

    assert file_path.name in page.inner_text('#uploadedFilePath')


def test_expect_element(page):
    page.goto('https://demoqa.com/dynamic-properties')
    expect(page.locator('#enableAfter')).to_be_enabled(timeout=6000)
    page.click('#enableAfter')
    page.reload()
    expect(page.locator('#visibleAfter')).to_be_visible(timeout=6000)
    page.click('#visibleAfter')
    page.reload()
    expect(page.locator('#colorChange')).to_have_css('color', 'rgb(220, 53, 69)', timeout=6000)


def test_alerts(page):
    page.goto('https://demoqa.com/alerts')

    def handle_alert_1(dialog):
        equal(dialog.message, 'You clicked a button')
        dialog.accept()

    def handle_alert_2(dialog):
        equal(dialog.message, 'This alert appeared after 5 seconds')
        dialog.accept()

    def handle_alert_3(dialog):
        equal(dialog.message, 'Do you confirm action?')
        dialog.accept()

    def handle_alert_4(dialog):
        equal(dialog.message, 'Please enter your name')
        dialog.accept('123')

    page.once('dialog', handle_alert_1)
    page.click('#alertButton')

    page.once('dialog', handle_alert_2)
    page.click('#timerAlertButton')
    page.wait_for_event('dialog', timeout=6000)

    page.once('dialog', handle_alert_3)
    page.click('#confirmButton')
    equal(page.inner_text('#confirmResult'), 'You selected Ok')

    page.once('dialog', handle_alert_4)
    page.click('#promtButton')
    equal(page.inner_text('#promptResult'), 'You entered 123')

def test_calendar(page):
    page.goto('https://demoqa.com/date-picker')

    calendar_obj = page.locator('#dateAndTimePickerInput')
    calendar_obj.click()

    page.locator('.react-datepicker__month-read-view').click()
    page.locator('.react-datepicker__month-option >> text=January').click()

    page.locator('.react-datepicker__year-read-view').click()
    page.locator('.react-datepicker__year-option >> text=2025').click()

    page.locator('.react-datepicker__day--001').first.click()

    page.locator('.react-datepicker__time-list-item  >> text=00:00').click()

    equal(calendar_obj.get_attribute('value'), 'January 1, 2025 12:00 AM')









