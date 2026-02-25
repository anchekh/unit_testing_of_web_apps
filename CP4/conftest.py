from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
import time

logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('log.txt'),
        logging.StreamHandler()
    ]
)

PRODUCT_URLS = [
    "https://vladmag.ru/product/holodilnik-midea-mdrb471mgf01o",
    "https://vladmag.ru/product/sirop-monin-butterscotch-iris-1000-ml"
]

logging.info("Проверка началась")
logging.debug("Открытие браузера")

try:
    driver = webdriver.Chrome()

    for url in PRODUCT_URLS:
        logging.info(f"Переход на страницу товара: {url}")
        driver.get(url)

        time.sleep(5)
        logging.debug("Страница загружена")

        logging.info("Проверка статуса товара")

        try:
            available_element = driver.find_element(By.CSS_SELECTOR, "div.product-available")
            element_classes = available_element.get_attribute("class")

            if "product-available--soldout" in element_classes:
                logging.info("Товара нет в наличии (soldout)")

                try:
                    preorder_button = driver.find_element(By.CSS_SELECTOR, "button[data-target='preorder']")
                    if preorder_button.is_enabled():
                        logging.info("Кнопка 'Предзаказ' найдена")
                        logging.info(f"Текст кнопки: {preorder_button.text}")

                    else:
                        logging.warning("Кнопка 'Предзаказ' неактивна")
                except:
                    logging.warning("Кнопка 'Предзаказ' не найдена")

            else:
                available_text = available_element.get_attribute("data-text-available")
                logging.info("Товар в наличии (product-available)")

                try:
                    buy_button = driver.find_element(By.CSS_SELECTOR, "button[data-item-add]")
                    if buy_button.is_enabled():
                        logging.info("Кнопка 'В корзину' найдена")
                        logging.info(f"Текст кнопки: {buy_button.text}")

                        logging.info("Нажатие на кнопку 'В корзину'")
                        buy_button.click()
                        time.sleep(3)
                        logging.info("Товар добавлен в корзину")
                    else:
                        logging.warning("Кнопка 'В корзину' неактивна")
                except:
                    logging.error("Кнопка 'В корзину' не найдена")

        except Exception as e:
            logging.error(f"Ошибка при работе с товаром: {str(e)}")

        time.sleep(3)

except Exception as e:
    logging.critical(f"Ошибка: {str(e)}")

finally:
    logging.debug("Закрытие браузера")
    driver.quit()
    logging.info("Проверка завершена")