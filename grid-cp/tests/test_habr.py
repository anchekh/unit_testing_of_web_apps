import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image
import imagehash

GRID_URL = "http://localhost:4444/wd/hub"
URL = "https://habr.com/"

SCREEN_DIR = "screens"
EXPECTED_PATH = os.path.join(SCREEN_DIR, "expected.png")
ACTUAL_PATH = os.path.join(SCREEN_DIR, "actual.png")


def get_driver():
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Remote(
        command_executor=GRID_URL,
        options=options
    )

    driver.set_window_size(1920, 1080)
    return driver


def wait_page_loaded(driver):
    WebDriverWait(driver, 15).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def take_screenshot(driver, path):
    time.sleep(2)
    driver.save_screenshot(path)


def compare_images(img1_path, img2_path, threshold=15):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)

    hash1 = imagehash.average_hash(img1)
    hash2 = imagehash.average_hash(img2)

    diff = hash1 - hash2
    return diff <= threshold, diff


@pytest.mark.ui
def test_habr_visual():
    os.makedirs(SCREEN_DIR, exist_ok=True)

    driver = get_driver()

    try:
        driver.get(URL)
        wait_page_loaded(driver)

        take_screenshot(driver, ACTUAL_PATH)

        if not os.path.exists(EXPECTED_PATH):
            os.rename(ACTUAL_PATH, EXPECTED_PATH)
            pytest.skip("baseline created")

        result, diff = compare_images(EXPECTED_PATH, ACTUAL_PATH)

        assert result, f"diff={diff}"

    finally:
        driver.quit()
