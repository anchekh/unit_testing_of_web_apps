import pytest

BASE_URL = "https://bagazh-dv.ru/"

@pytest.mark.parametrize(
    "link_text, expected_in_title",
    [
        ("О компании", "О компании"),
        ("Каталог", "Каталог"),
        ("Оплата и доставка", "Оплата"),
        ("Контакты", "Контакты"),
    ],
)
def test_top_navigation(driver, link_text, expected_in_title):
    driver.get(BASE_URL)

    link = driver.find_element("link text", link_text)
    link.click()

    assert expected_in_title.lower() in driver.title.lower(), (
        f"Ошибка: переход по ссылке '{link_text}' открыл неверную страницу"
    )

@pytest.mark.parametrize(
    "category_text",
    [
        "Женские сумки",
        "Дорожные и спортивные сумки",
        "Мужские рюкзаки",
    ],
)
def test_category_links(driver, category_text):
    driver.get(BASE_URL)

    category_link = driver.find_element("link text", category_text)
    category_link.click()

    product_cards = driver.find_elements(
        "css selector",
        ".products .product"
    )

    assert product_cards, (
        f"Ошибка: в категории '{category_text}' не найдены товары"
    )