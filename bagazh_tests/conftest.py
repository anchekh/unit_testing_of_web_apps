import os
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox"],
        help="Браузер для запуска тестов",
    )

@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--browser").lower()

@pytest.fixture(scope="function")
def driver(browser_name, request):
    remote_url = os.environ.get("REMOTE_URL")

    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        if remote_url:
            driver = webdriver.Remote(
                command_executor=remote_url,
                options=options
            )
        else:
            driver = webdriver.Chrome(
                service=webdriver.chrome.service.Service(
                    ChromeDriverManager().install()
                ),
                options=options
            )

    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.add_argument("-headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        if remote_url:
            driver = webdriver.Remote(
                command_executor=remote_url,
                options=options
            )
        else:
            driver = webdriver.Firefox(
                service=webdriver.firefox.service.Service(
                    GeckoDriverManager().install()
                ),
                options=options
            )

    else:
        raise ValueError(
            f"Ошибка: браузер '{browser_name}' не поддерживается"
        )

    driver.implicitly_wait(10)

    yield driver

    if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
        screenshots_dir = os.path.join(
            os.getcwd(),
            "screenshots"
        )

        os.makedirs(
            screenshots_dir,
            exist_ok=True
        )

        screenshot_file = os.path.join(
            screenshots_dir,
            f"{request.node.name}_{browser_name}.png"
        )

        driver.save_screenshot(screenshot_file)

    driver.quit()

def pytest_runtest_makereport(item, call):
    if "driver" in item.fixturenames:
        outcome = yield
        rep = outcome.get_result()
        setattr(item, f"rep_{rep.when}", rep)