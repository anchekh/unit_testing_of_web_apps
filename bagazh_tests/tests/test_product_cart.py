from selenium.webdriver.common.by import By
import pytest

BASE_URL = "https://bagazh-dv.ru/"

def _open_first_product(driver):
    driver.get(BASE_URL)

    new_items_link = driver.find_element(By.LINK_TEXT, "Новинки")
    new_items_link.click()

    first_product = driver.find_elements(
        By.CSS_SELECTOR,
        ".product a.product-card__image"
    )[0]

    first_product.click()

def test_add_product_to_cart(driver):
    _open_first_product(driver)

    buy_button = driver.find_element(
        By.CSS_SELECTOR,
        "button.btn-buy"
    )
    buy_button.click()

    cart_indicator = driver.find_element(
        By.CSS_SELECTOR,
        "#cart-mini"
    )

    assert "Корзина" in cart_indicator.text, (
        "Ошибка: виджет корзины не появился после добавления товара"
    )

    assert any(ch.isdigit() for ch in cart_indicator.text), (
        "Ошибка: в корзине не отображается количество товаров"
    )

    cart_indicator.find_element(By.TAG_NAME, "a").click()

    cart_items = driver.find_elements(
        By.CSS_SELECTOR,
        ".cart-products .cart-item"
    )

    assert cart_items, (
        "Ошибка: товар отсутствует в корзине после добавления"
    )

def test_remove_product_from_cart(driver):
    _open_first_product(driver)

    driver.find_element(
        By.CSS_SELECTOR,
        "button.btn-buy"
    ).click()

    driver.find_element(
        By.CSS_SELECTOR,
        "#cart-mini a"
    ).click()

    remove_btn = driver.find_element(
        By.CSS_SELECTOR,
        ".cart-item .remove-btn, .cart-item .icon-trash"
    )

    remove_btn.click()

    empty_message = driver.find_element(
        By.CSS_SELECTOR,
        ".cart-empty, .empty-cart"
    )

    assert empty_message.is_displayed(), (
        "Ошибка: корзина не стала пустой после удаления товара"
    )