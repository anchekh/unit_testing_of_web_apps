import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv

load_dotenv()

LOGIN = os.getenv("PIKABU_LOGIN")
PASSWORD = os.getenv("PIKABU_PASSWORD")
PIKABU_URL = "https://pikabu.ru/"

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    print("Открытие сайта")
    driver.get(PIKABU_URL)
    
    time.sleep(10)

    print("1. Тестирование авторизации")
    
    print("Ввод логина")
    login_field = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
    )
    login_field.clear()
    login_field.send_keys(LOGIN)
    print(f"Логин '{LOGIN}' введен")
    
    print("Ввод пароля")
    password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
    password_field.clear()
    password_field.send_keys(PASSWORD)
    print("Пароль введен")
    
    print("Нажатие на кнопку 'войти'")
    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].button_success"))
    )
    submit_button.click()
    print("Кнопка входа нажата")

    time.sleep(30)
    
    print("Проверка авторизации")
    avatar = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.header-right-menu__item.avatar_indicate-on-hover"))
    )
    print("Авторизация успешна")
    
    time.sleep(2)

    print("2. Тестирование поиска")
    
    print("Нажатие на кнопку поиска")
    search_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.header-right-menu__item.header-right-menu__search"))
    )
    search_button.click()
    print("Кнопка поиска нажата")
    
    time.sleep(2)
    
    print("Ввод поискового запроса")
    search_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.Input__input--NFSQdJl_[placeholder='Искать на Пикабу']"))
    )
    search_input.clear()
    search_input.send_keys("айти")
    print("Слово 'айти' введено")
    
    print("Нажатие на кнопку 'найти'")
    find_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Btn__btn--AXJA8qM4.Btn__btn_primary--Zfmrd9NN"))
    )
    find_button.click()
    print("Кнопка 'найти' нажата")
    
    time.sleep(5)
    
    expected_url = "https://pikabu.ru/search?q=%D0%B0%D0%B9%D1%82%D0%B8&st=3"
    current_url = driver.current_url
    
    if current_url == expected_url:
        print("Поиск выполнен успешно")
    else:
        print(f"Ошибка: ожидался url {expected_url}, получен {current_url}")

    time.sleep(5)
    
    print("3. Тестирование кнопок меню")
    
    menu_items = [
        {"name": "Горячее", "expected_url": "https://pikabu.ru/"},
        {"name": "Лучшее", "expected_url": "https://pikabu.ru/best"},
        {"name": "Свежее", "expected_url": "https://pikabu.ru/new"},
        {"name": "Подписки", "expected_url": "https://pikabu.ru/subs"},
        {"name": "Сообщества", "expected_url": "https://pikabu.ru/communities"},
        {"name": "Блоги", "expected_url": "https://pikabu.ru/companies"},
        {"name": "Темы", "expected_url": "https://pikabu.ru/themes"}
    ]
    
    for item in menu_items:
        try:
            print(f"Переход на '{item['name']}'")
            
            driver.get("https://pikabu.ru/")
            time.sleep(2)
            
            menu_link = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//a[text()='{item['name']}']"))
            )
            menu_link.click()
            
            time.sleep(3)
            
            current_url = driver.current_url
            if current_url == item["expected_url"]:
                print(f"Успешно: {current_url}")
            else:
                print(f"Ошибка: ожидался {item['expected_url']}, получен {current_url}")
            
            time.sleep(1)
            
        except TimeoutException:
            print(f"Ошибка: кнопка '{item['name']}' не найдена")
    
    print("Тестирование меню завершено")

    time.sleep(5)
    
    print("4.Тестирование перехода на тему 'it'")
    
    try:
        print("Переход на вкладку 'темы'")
        driver.get("https://pikabu.ru/")
        time.sleep(2)
        
        themes_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Темы']"))
        )
        themes_link.click()
        time.sleep(3)
        
        current_url = driver.current_url
        if current_url == "https://pikabu.ru/themes":
            print("Успешно: переход на страницу тем выполнен")
        else:
            print(f"Ошибка: ожидался https://pikabu.ru/themes, получен {current_url}")
        
        print("Нажатие на тему 'it'")
        it_theme = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/themes/it']"))
        )
        it_theme.click()
        time.sleep(3)
        
        current_url = driver.current_url
        if current_url == "https://pikabu.ru/themes/it":
            print("Успешно: переход на тему 'it' выполнен")
        else:
            print(f"Ошибка: ожидался https://pikabu.ru/themes/it, получен {current_url}")
        
    except TimeoutException as e:
        print(f"Ошибка: {e}")
    
    print("Тестирование темы 'it' завершено")
    
except TimeoutException as e:
    print(f"Ошибка: элемент не найден - {e}")
    
finally:
    time.sleep(5)
    print("Тестирование сайта завершено")
    driver.quit()
    print("Браузер закрыт")
