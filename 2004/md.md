# Библиотеки для визуального тестирования

## 1. Selenium

**Назначение:** автоматизация браузера.

**Основные возможности:** - Открытие страниц - Поиск элементов -
Взаимодействие (клики, ввод текста) - Получение скриншотов

**Базовые команды:**

``` python
driver = webdriver.Chrome()
driver.get("https://example.com")

element = driver.find_element("id", "login")
element.click()

driver.save_screenshot("screen.png")
driver.quit()
```

------------------------------------------------------------------------

## 2. pytest

**Назначение:** фреймворк для написания тестов.

**Основные возможности:** - Простая структура тестов - Фикстуры -
Параметризация

**Пример:**

``` python
def test_example():
    assert 1 + 1 == 2
```

------------------------------------------------------------------------

## 3. pytest-selenium

**Назначение:** интеграция Selenium с pytest.

**Плюсы:** - Готовые фикстуры (driver) - Упрощённый запуск тестов

**Пример:**

``` python
def test_open_page(selenium):
    selenium.get("https://example.com")
    assert "Example" in selenium.title
```

------------------------------------------------------------------------

## 4. Pillow (PIL)

**Назначение:** работа с изображениями.

**Основные возможности:** - Открытие/сохранение изображений -
Сравнение - Редактирование

**Пример:**

``` python
from PIL import Image

img = Image.open("image.png")
img.save("copy.png")
```

------------------------------------------------------------------------

## 5. ImageHash

**Назначение:** сравнение изображений через хеш.

**Идея:** - Преобразует изображение в хеш - Сравнение по "расстоянию"

**Пример:**

``` python
import imagehash
from PIL import Image

hash1 = imagehash.average_hash(Image.open('img1.png'))
hash2 = imagehash.average_hash(Image.open('img2.png'))

print(hash1 - hash2)  # чем меньше, тем больше похожи
```

------------------------------------------------------------------------

## 6. pytest-regressions

**Назначение:** регрессионное тестирование (в т.ч. изображений).

**Возможности:** - Сравнение текущего результата с эталоном -
Авто-сохранение baseline

**Пример:**

``` python
def test_image(image_regression):
    with open("image.png", "rb") as f:
        image_regression.check(f.read())
```

------------------------------------------------------------------------

## 7. scikit-image

**Назначение:** обработка изображений и анализ.

**Основные возможности:** - Метрики сходства (SSIM) - Фильтры -
Преобразования

**Пример:**

``` python
from skimage.metrics import structural_similarity as ssim
import cv2

img1 = cv2.imread("img1.png", 0)
img2 = cv2.imread("img2.png", 0)

score, _ = ssim(img1, img2, full=True)
print(score)
```

------------------------------------------------------------------------

## 8. Дополнительно

### os

Работа с файловой системой:

``` python
import os

os.listdir()
os.path.join("dir", "file.png")
```

------------------------------------------------------------------------

### WebDriverWait + expected_conditions

Ожидание элементов:

``` python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(("id", "login"))
)
```

------------------------------------------------------------------------

## Общий пайплайн визуального теста

1.  Открыть страницу (Selenium)
2.  Сделать скриншот
3.  Сравнить:
    1) через PIL
    2) через ImageHash
    3) через SSIM (scikit-image)
4.  Проверить отклонение
5.  Логировать результат (pytest)

------------------------------------------------------------------------

## Важные факторы тестирования

1. Разрешение экрана
2. Браузер и ОС
3. Шрифты и масштабирование
4. Адаптивная верстка
