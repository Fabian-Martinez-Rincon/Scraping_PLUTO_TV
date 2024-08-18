import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

def click_button(driver, selector_type, selector):
    """
    Clicks on a button based on the provided selector type and value.

    Args:
    driver: The WebDriver instance.
    selector_type (str): Type of selector to use (e.g., "XPATH", "CSS_SELECTOR").
    selector (str): The selector value.

    This function attempts to click on an element specified by the selector.
    If the element is not found or not clickable, it handles the
    exception and prints an error message.
    """
    try:
        by_method = getattr(By, selector_type.upper(), None)
        if not by_method:
            raise ValueError(f"Unsupported selector type provided: {selector_type}")

        button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((by_method, selector))
        )
        time.sleep(1)
        button.click()
        print(f"Clicked on button with {selector_type}: {selector}")
        time.sleep(1)
    except TimeoutException as e:
        print(f"Timeout waiting for button with {selector_type} '{selector}': {str(e)}")
    except WebDriverException as e:
        print(f"Error when clicking on button with {selector_type} '{selector}': {str(e)}")
