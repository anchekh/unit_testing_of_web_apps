from appium import webdriver
from appium.options.ios import XCUITestOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = XCUITestOptions()
options.platform_name = "iOS"
options.device_name = "iPhone 14"
options.bundle_id = "com.vk.vkclient"

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
wait = WebDriverWait(driver, 20)

login_btn = wait.until(EC.presence_of_element_located((By.ACCESSIBILITY_ID, "Войти")))
phone_field = wait.until(EC.presence_of_element_located((By.ACCESSIBILITY_ID, "Телефон или почта")))
signup_btn = wait.until(EC.presence_of_element_located((By.ACCESSIBILITY_ID, "Зарегистрироваться")))
logo = wait.until(EC.presence_of_element_located((By.ACCESSIBILITY_ID, "VK")))

assert login_btn.is_displayed()
assert phone_field.is_displayed()
assert signup_btn.is_displayed()
assert logo.is_displayed()

driver.quit()
