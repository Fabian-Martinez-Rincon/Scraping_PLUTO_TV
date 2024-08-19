import time
import json
import logging
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_to_json(data, file_name, folder_name=None):
    """
    Saves the scraped data to a JSON file in the 'data' directory, optionally within a 
    specified subfolder.

    Args:
        data (list): The data to save.
        file_name (str): The name of the file to save the data in.
        folder_name (str, optional): The name of the subfolder within 'data' to save the file.
        Defaults to None.
    """
    base_directory = 'data'

    if folder_name:
        directory = os.path.join(base_directory, folder_name)
    else:
        directory = base_directory

    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, file_name)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logging.info('Data successfully saved to %s', file_path)
    except IOError as e:
        logging.error('Failed to save data to %s: %s', file_path, str(e))


def combine_json_files(input_folder, combined_filename, output_folder=None):
    """
    Combines all JSON files in the specified input folder (inside the 'data' directory) into a single JSON file.

    Args:
        input_folder (str): The folder inside 'data' containing the JSON files to combine.
        combined_filename (str): The name of the output combined JSON file.
        output_folder (str, optional): The folder to save the combined JSON file. Defaults to the current directory.
    """
    # Define the base directory for input files
    base_input_directory = os.path.join('data', input_folder)
    
    combined_data = {}

    # Loop through all files in the input folder
    for filename in os.listdir(base_input_directory):
        if filename.endswith(".json"):
            filepath = os.path.join(base_input_directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                category_name = os.path.splitext(filename)[0]  # Remove the .json extension
                combined_data[category_name] = data

    # Determine the output directory
    if output_folder:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        combined_filepath = os.path.join(output_folder, combined_filename)
    else:
        combined_filepath = os.path.join(os.getcwd(), combined_filename)

    # Save the combined data to the output file
    with open(combined_filepath, "w", encoding="utf-8") as outfile:
        json.dump(combined_data, outfile, ensure_ascii=False, indent=4)

    print(f"Combined JSON file saved to {combined_filepath}")

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

    # Wait for and click the button
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
