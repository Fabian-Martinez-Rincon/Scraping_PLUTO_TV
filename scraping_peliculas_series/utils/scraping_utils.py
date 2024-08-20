import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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


def wait_for_element_by_xpath(driver, xpath, timeout=10):
    """
    Waits for an element to be visible by its XPath.

    Args:
    driver: The WebDriver instance.
    xpath (str): The XPath of the element to wait for.
    timeout (int): The maximum time to wait for the element.

    Returns:
    WebElement: The WebElement once it is visible.
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
    except TimeoutException:
        print(f"Timeout waiting for element with XPath: {xpath}")
        return None

def get_nav_items(nav_element):
    """
    Extracts navigation items from a navigation element.

    Args:
    nav_element: The WebElement containing the navigation items.

    Returns:
    list: A list of dictionaries, each containing the text and link of navigation items.
    """
    nav_items = nav_element.find_elements(By.TAG_NAME, "a")
    buttons = [{'Categoria': item.text, 'Link': item.get_attribute('href')} for item in nav_items]
    return buttons

def click_button_and_get_nav_items(driver, button_xpath):
    """
    Clicks on a button specified by an XPath and retrieves navigation 
    items from a subsequent navigation area.

    Args:
    driver: Instance of Selenium WebDriver.
    button_xpath (str): XPath to the button that needs to be clicked.

    Returns:
    list: A list of dictionaries, each containing the text and link of navigation items.
    """
    nav_xpath = "/html/body/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[1]/div/nav"

    button = wait_for_element_by_xpath(driver, button_xpath)
    if button:
        button.click()

    # Wait for the navigation area to be visible
    nav_element = wait_for_element_by_xpath(driver, nav_xpath)
    if nav_element:
        buttons = get_nav_items(nav_element)
        for button in buttons:
            original_href = button['Link']
            button['Link'] = f"https://pluto.tv/latam{original_href[16:]}?lang=en"
            print(f"Categoría: {button['Categoria']}\nLink: {button['Link']}\n{'-'*40}")
        return buttons
    else:
        return []

def find_element_with_retries(driver, xpath, retries=1):
    """
    Attempts to find an element on the page using its XPATH. If found, scrolls into view smoothly.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        xpath (str): The XPATH of the element to be found.
        retries (int): The number of retries to attempt before giving up.
    
    Returns:
        WebElement: The found element if successful, otherwise None.
    """
    attempt = 0
    while attempt < retries:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                element
            )
            return element
        except TimeoutException:
            print(f"Attempt {attempt + 1}: Element not found, scrolling and retrying...")
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.PAGE_DOWN)
            attempt += 1
        except Exception as e:
            print(f"Unexpected error on attempt {attempt + 1}: {e}")
            break
    return None