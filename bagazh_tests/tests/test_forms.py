from selenium.webdriver.common.by import By
import pytest

BASE_URL = "https://bagazh-dv.ru/"

def test_login_form_rendering(driver):
    driver.get(BASE_URL)

    login_link = driver.find_element(By.LINK_TEXT, "Войдите")
    login_link.click()

    username_input = driver.find_element(
        By.CSS_SELECTOR,
        "input[name='login'], input[type='email']"
    )
    password_input = driver.find_element(
        By.CSS_SELECTOR,
        "input[type='password']"
    )

    assert (
        username_input.is_displayed() and password_input.is_displayed()
    ), "Ошибка: поля логина и пароля не отображаются"

def test_registration_form_validation(driver):
    driver.get(BASE_URL)

    reg_link = driver.find_element(By.LINK_TEXT, "Зарегистрируйтесь")
    reg_link.click()

    submit_btn = driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    )
    submit_btn.click()

    alerts = driver.find_elements(
        By.CSS_SELECTOR,
        ".error, .invalid-feedback, .alert-danger"
    )

    assert alerts, "Ошибка: форма регистрации приняла пустые данные"

def test_newsletter_email_validation(driver):
    driver.get(BASE_URL)

    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);"
    )

    email_input = driver.find_element(
        By.CSS_SELECTOR,
        "form input[type='email']"
    )

    email_input.send_keys("invalid")

    subscribe_btn = driver.find_element(
        By.CSS_SELECTOR,
        "form button[type='submit']"
    )
    subscribe_btn.click()

    assert (
        email_input.get_attribute("value") == "invalid"
    ), "Ошибка: некорректный email был принят формой"