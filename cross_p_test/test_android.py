from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "Android Emulator"
options.app_package = "com.vkontakte.android"
options.app_activity = "com.vk.core.fragments.AuthActivity"

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
wait = WebDriverWait(driver, 20)

login_btn = wait.until(EC.presence_of_element_located((By.ID, "com.vkontakte.android:id/login_button")))
phone_field = wait.until(EC.presence_of_element_located((By.ID, "com.vkontakte.android:id/phone_input")))
signup_btn = wait.until(EC.presence_of_element_located((By.ID, "com.vkontakte.android:id/sign_up_button")))
logo = wait.until(EC.presence_of_element_located((By.ID, "com.vkontakte.android:id/logo")))

assert login_btn.is_displayed()
assert phone_field.is_displayed()
assert signup_btn.is_displayed()
assert logo.is_displayed()

driver.quit()
