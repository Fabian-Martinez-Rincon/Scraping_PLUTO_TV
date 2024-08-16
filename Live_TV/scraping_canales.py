from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def config():
    driver_path = 'chromedriver.exe'
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def main():
    driver = config()
    driver.get('https://pluto.tv')
    time.sleep(5)
    on_demand= WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/button/span/span')
        )
    )
    on_demand.click()

    select= WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div/div/div/main/div[2]/div/div[2]/section/div[3]/div/div[2]/div/div[1]/div/h3')
        )
    )
    select.click()

    body = driver.find_element(By.TAG_NAME, 'body')
    #//a[@href="/live-tv/5dcde437229eff00091b6c30/details"]
    time.sleep(2)
    element_to_click = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[@aria-rowindex="2"]')
            )
        )
    link_element = element_to_click.find_element(By.TAG_NAME, 'a')
    
    # Extrae el valor del atributo href
    href_value = link_element.get_attribute('href')
    print("Valor del atributo href:")
    print(href_value)

    # Realizar scroll hasta que el botón no esté seleccionado
    #for i in range(1000):
    #    body.send_keys(Keys.ARROW_DOWN)
    #    time.sleep(0.01)


    time.sleep(5)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()

if __name__ == "__main__":
    main()
