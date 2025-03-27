from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime
import time

from app_loader import AppLoader

# List of your Streamlit app URLs
KEEP_ALIVE_CATEGORIES = ('proteomics')
HOME_URL = 'https://proteomics-tools.streamlit.app/'

all_apps = AppLoader.load_from_yaml('conf.yml')['apps']
app_urls = [HOME_URL]
app_urls.extend([app.url for app in all_apps if app.category in KEEP_ALIVE_CATEGORIES])


def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--v=1")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def wake_up_apps(driver):
    for url in app_urls:
        try:
            driver.get(url)
            print(f"{datetime.now()}: Accessing {url}")

            # Wait and print page source to debug
            time.sleep(5)
            page_source = driver.page_source
            print("Page source length:", len(page_source))

            # Save page source to file for inspection
            with open('page_source.html', 'w', encoding='utf-8') as f:
                f.write(page_source)

            # Multiple button locator strategies
            button_locators = [
                (By.CSS_SELECTOR, 'button[data-testid="wakeup-button-owner"]'),
                (By.XPATH, '//button[contains(text(), "Wake Up")]'),
                (By.XPATH, '//button[contains(@class, "wake-up")]'),
                (By.XPATH, '//button'),  # Fallback to any button
            ]

            button_found = False
            for locator in button_locators:
                try:
                    # Try to find all elements matching the locator
                    buttons = driver.find_elements(*locator)
                    print(f"Buttons found with {locator}: {len(buttons)}")

                    # Print details of found buttons
                    for i, button in enumerate(buttons):
                        print(f"Button {i + 1} details:")
                        print(f"  Text: {button.text}")
                        print(f"  Is displayed: {button.is_displayed()}")
                        print(f"  Is enabled: {button.is_enabled()}")
                        print(f"  Attributes: {button.get_attribute('outerHTML')}")

                    # If buttons found, attempt to click
                    if buttons:
                        for button in buttons:
                            try:
                                # Scroll into view
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)

                                # Try clicking
                                button.click()
                                print(f"Successfully clicked button with locator {locator}")
                                button_found = True
                                break
                            except Exception as click_error:
                                print(f"Failed to click button: {click_error}")

                    if button_found:
                        break

                except Exception as find_error:
                    print(f"Error finding buttons with {locator}: {find_error}")

            if not button_found:
                print("No suitable button found")

        except Exception as e:
            print(f"{datetime.now()}: Error accessing {url}: {e}")


def main():
    driver = initialize_driver()
    try:
        wake_up_apps(driver)
        time.sleep(10)  # Keep browser open to inspect
    finally:
        driver.quit()


if __name__ == "__main__":
    main()