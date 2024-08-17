import time
import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, WebDriverException)


def click_button_by_text(driver, button_text):
    """
    Clicks on a button identified by its text using Selenium WebDriver.

    Args:
    driver: The WebDriver instance.
    button_text (str): The text of the button to click.

    This function waits until the button is visible, moves to the button, and performs a click.
    If the button is not found or the click fails, it prints an error message.
    """
    try:
        button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//span[text()='{button_text}']"))
        )
        ActionChains(driver).move_to_element(button).click().perform()
        print(f"Clicked on: {button_text}")
    except TimeoutException as e:
        print(f"Timeout waiting for button '{button_text}': {str(e)}")
    except WebDriverException as e:
        print(f"Web driver error when clicking on '{button_text}': {str(e)}")


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
    driver.find_element(By.XPATH, button_xpath).click()

    nav_xpath = "/html/body/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[1]/div/nav"
    nav = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, nav_xpath))
    )

    nav_items = nav.find_elements(By.TAG_NAME, "a")
    buttons = [{'Categoria': item.text, 'Link': item.get_attribute('href')} for item in nav_items]
    for button in buttons:
        print(f"Categoría: {button['Categoria']}\nLink: {button['Link']}\n{'-'*40}")
    return buttons


def config():
    """
    Configura y retorna un driver de Selenium para Chrome con opciones específicas.

    Configura el navegador para abrirse en modo incógnito y maximizado.

    Returns:
    WebDriver: Una instancia del driver de Chrome configurada.
    """
    driver_path = 'chromedriver.exe'
    service = Service(driver_path)
    options = webdriver.ChromeOptions()

    options.add_argument("--incognito")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=service, options=options)
    return driver

def start():
    """
    Starts a Selenium WebDriver to interact with the Pluto TV website,
    fetches navigation items, and saves them to a JSON file.
    
    Returns:
    tuple: The driver instance and the list of navigation buttons and links.
    """
    driver = config()
    driver.get('https://pluto.tv')

    on_demand= WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, 'On Demand')
        )
    )
    on_demand.click()
    time.sleep(1)
    click_button_by_text(driver, "Series")
    time.sleep(1)
    series_link_xpath = ('/html/body/div[1]/div/div/div/main/div[3]/div/section/div/div/div/div'
                         '/section[3]'
                         '/span/div/div[1]/span/a')
    driver.find_element(By.XPATH, series_link_xpath).click()
    time.sleep(1)
    button_xpath = '/html/body/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[1]/div/button'
    buttons = click_button_and_get_nav_items(driver, button_xpath)
    time.sleep(1)
    for item in buttons:
        original_href = item['Link']
        item['Link'] = f"https://pluto.tv/latam{original_href[16:]}?lang=en"
    current_button= WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, button_xpath))
                ).text
    current_element = {'Categoria': current_button, 'Link': driver.current_url}
    buttons.insert(0, current_element)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'categories.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(buttons, file, ensure_ascii=False, indent=4)
    time.sleep(3)
    return driver

def main():
    """
    Main function to start the web driver, perform operations, and then quit the driver.
    """
    driver = start()

    driver.quit()


if __name__ == "__main__":
    main()
