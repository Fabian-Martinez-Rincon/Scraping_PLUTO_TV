
import os
import logging

from config_driver import config
from utils import click_button, click_button_and_get_nav_items
from utils import save_to_json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PLUTO_TV_URL = 'https://pluto.tv'
ON_DEMAND_BUTTON_XPATH = "/html/body/div[1]/div/div/div/header/nav/span[2]/a/span"
SERIES_BUTTON_XPATH = "//span[text()='Series']"
VIEW_ALL_BUTTON_XPATH = "/html/body/div[1]/div/div/div/main/div[3]/div/section/div/div/div/div/section[3]/span/div/div[1]/span/a"
MENU_BUTTON_XPATH = "/html/body/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[1]/div/button"

class XPathConfig:
    ON_DEMAND_BUTTON = "//nav/span[2]/a/span"
    SERIES_BUTTON = "//span[text()='Series']"
    VIEW_ALL_BUTTON = "//section[3]/span/div/div[1]/span/a"
    MENU_BUTTON = "//div[1]/div/div[1]/div/nav"

OUTPUT_FILE = 'categories.json'

def navigate_and_scrape(driver):
    """
    Navigates through the Pluto TV site and scrapes the necessary data.

    Args:
    driver: The WebDriver instance.

    Returns:
    list: A list of navigation buttons and links.
    """
    try:
        click_button(driver, "XPATH", ON_DEMAND_BUTTON_XPATH)
        click_button(driver, "XPATH", SERIES_BUTTON_XPATH)
        click_button(driver, "XPATH", VIEW_ALL_BUTTON_XPATH)
        buttons = click_button_and_get_nav_items(driver, MENU_BUTTON_XPATH)
        return buttons
    except Exception as e:
        logging.error('An error occurred while scraping: %s', str(e))
        return []

def start_scraping():
    """
    Initializes the Selenium WebDriver, performs the scraping,
    and saves the scraped data to a JSON file.
    """
    driver = None
    try:
        driver = config()
        driver.get(PLUTO_TV_URL)

        buttons = navigate_and_scrape(driver)
        if buttons:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, OUTPUT_FILE)
            save_to_json(buttons, file_path)
        else:
            logging.warning("No data was scraped.")
    except Exception as e:
        logging.error("An error occurred during the scraping process: %s", {str(e)})
    finally:
        if driver:
            driver.quit()

def main():
    """
    Main function to start the scraping process.
    """
    start_scraping()

if __name__ == "__main__":
    main()
