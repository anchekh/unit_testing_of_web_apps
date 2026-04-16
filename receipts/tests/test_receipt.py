import pytest
import allure
from receipt import validate, calculate


@allure.feature("Кассовый модуль")
class TestReceipt:

    @allure.story("Валидация")
    def test_empty_receipt(self):
        with pytest.raises(ValueError):
            validate([])

    @allure.story("Валидация")
    def test_negative_price(self):
        with pytest.raises(ValueError):
            validate([{"name": "test", "price": -1}])

    @allure.story("Расчет стоимости")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_discount(self):
        items = [
            {"name": "A", "price": 6000},
            {"name": "B", "price": 6000},
        ]

        validate(items)

        with allure.step("Расчет итога"):
            subtotal, discounted, nds, total = calculate(items)

        assert subtotal == 12000
        assert discounted == 10800
        assert nds == 2160
        assert total == 12960

    @allure.story("Расчет стоимости")
    def test_no_discount(self):
        items = [{"name": "A", "price": 5000}]
        _, discounted, _, _ = calculate(items)
        assert discounted == 5000

    @allure.story("Расчет стоимости")
    def test_print_receipt(self):
        from receipt import print_receipt

        data = {
            "items": [
                {"name": "Услуга", "price": 1000}
            ],
            "payment": "Карта"
        }

        print_receipt(data)