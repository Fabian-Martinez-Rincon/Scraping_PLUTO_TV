from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import os


def click_button_by_text(driver, button_text):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//span[text()='{button_text}']"))
        )
        ActionChains(driver).move_to_element(button).click().perform()
        print(f"Clicked on: {button_text}")
        
    except Exception as e:
        print(f"Error al hacer clic en '{button_text}': {str(e)}")

def click_button_and_get_nav_items(driver, button_xpath):
    driver.find_element(By.XPATH, button_xpath).click()
    nav = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[1]/div/nav"))
    )
    nav_items = nav.find_elements(By.TAG_NAME, "a")
    
    buttons = [{'Categoria': item.text, 'Link': item.get_attribute('href')} for item in nav_items]
    return buttons

def config():
    driver_path = 'chromedriver.exe'
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def start():
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
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[3]/div/section/div/div/div/div/section[3]/span/div/div[1]/span/a').click()
    time.sleep(1)
    
    button_xpath = '/html/body/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[1]/div/button'
    buttons = click_button_and_get_nav_items(driver, button_xpath)
    for item in buttons:
        original_href = item['Link']
        item['Link'] = f"https://pluto.tv/latam{original_href[16:]}?lang=en"
    
    current_button= WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[1]/div/button'))
                ).text
    current_element = {'Categoria': current_button, 'Link': driver.current_url}
    buttons.insert(0, current_element)  
    
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'categories.json')
    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(buttons, file, ensure_ascii=False, indent=4)
    time.sleep(3)
    return driver, buttons

def main():
    driver, data = start()    
    print('Todo termino con exito')
    driver.quit()
    
if __name__ == "__main__":
    main()