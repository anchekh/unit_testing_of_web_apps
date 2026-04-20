import os
import pytest
import allure

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from PIL import Image, ImageChops
import imagehash

os.makedirs("baselines", exist_ok=True)
os.makedirs("diffs", exist_ok=True)

@pytest.fixture
def browser():
    opts = Options()
    opts.add_argument("--headless")

    driver = webdriver.Firefox(options=opts)
    driver.set_window_size(1920, 1080)

    yield driver
    driver.quit()

@allure.feature("UI тест")
@allure.story("Скриншотное тестирование")
def test_habr_ui(browser):
    browser.get("https://habr.com")

    wait = WebDriverWait(browser, 15)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    base = "baselines/habr.png"
    curr = "diffs/habr_current.png"
    diff = "diffs/habr_diff.png"

    browser.get_screenshot_as_file(curr)

    if not os.path.exists(base):
        os.replace(curr, base)
        pytest.skip("Эталонный скриншот создан")

    img_1 = Image.open(base).convert("RGB")
    img_2 = Image.open(curr).convert("RGB")

    hash_1 = imagehash.phash(img_1)
    hash_2 = imagehash.phash(img_2)

    allure.attach.file(curr, name="Текущий скриншот", attachment_type=allure.attachment_type.PNG)
    allure.attach.file(base, name="Эталон", attachment_type=allure.attachment_type.PNG)

    if (hash_1 - hash_2) > 5:
        diff_img = ImageChops.difference(img_1, img_2)
        diff_img.save(diff)

        allure.attach.file(diff, name="Разница", attachment_type=allure.attachment_type.PNG)

        assert False, f"Найдены визуальные отличия: {diff}"