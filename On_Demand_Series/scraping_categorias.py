import time
import json
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, WebDriverException)

from config_driver import config
from utils import click_button


def click_button_and_get_nav_items(driver):
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
    nav = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, nav_xpath))
    )

    nav_items = nav.find_elements(By.TAG_NAME, "a")
    buttons = [{'Categoria': item.text, 'Link': item.get_attribute('href')} for item in nav_items]
    for button in buttons:
        print(f"Categoría: {button['Categoria']}\nLink: {button['Link']}\n{'-'*40}")
    return buttons

def start():
    """
    Starts a Selenium WebDriver to interact with the Pluto TV website,
    fetches navigation items, and saves them to a JSON file.
    
    Returns:
    tuple: The driver instance and the list of navigation buttons and links.
    """
    driver = config()
    driver.get('https://pluto.tv')

    click_button(driver, "XPATH", "/html/body/div[1]/div/div/div/header/nav/span[2]/a/span")
    series = "Series"
    click_button(driver, "XPATH", f"//span[text()='{series}']")
    click_button(driver, "XPATH", "/html/body/div[1]/div/div/div/main/div[3]/div/section/div/div/div/div/section[3]/span/div/div[1]/span/a")
    button_xpath = "/html/body/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[1]/div/button"
    click_button(driver, "XPATH", button_xpath)
    

    buttons = click_button_and_get_nav_items(driver)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'categories.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(buttons, file, ensure_ascii=False, indent=4)
    return driver

def main():
    """
    Main function to start the web driver, perform operations, and then quit the driver.
    """
    driver = start()
    driver.quit()


if __name__ == "__main__":
    main()
