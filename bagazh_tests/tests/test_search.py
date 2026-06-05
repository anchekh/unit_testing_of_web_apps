from selenium.webdriver.common.by import By
import pytest

BASE_URL = "https://bagazh-dv.ru/"

@pytest.mark.parametrize(
    "query, expected_phrase",
    [
        ("сумка", "сумка"),
        ("рюкзак", "рюкзак"),
    ],
)
def test_search_results(driver, query, expected_phrase):
    driver.get(BASE_URL)

    search_input = driver.find_element(
        By.CSS_SELECTOR,
        "input[type='search'], input[name='q']"
    )

    search_input.clear()
    search_input.send_keys(query)
    search_input.submit()

    result_titles = [
        el.text
        for el in driver.find_elements(
            By.CSS_SELECTOR,
            ".product-card__title"
        )
    ]

    assert result_titles, (
        f"Ошибка: по запросу '{query}' не найдено ни одного результата"
    )

    assert any(
        expected_phrase.lower() in title.lower()
        for title in result_titles
    ), (
        f"Ошибка: результаты поиска по запросу '{query}' не содержат ожидаемое слово '{expected_phrase}'"
    )