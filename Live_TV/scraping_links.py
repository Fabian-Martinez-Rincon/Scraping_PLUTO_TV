from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
from collections import defaultdict
import requests
import os

def config():
    driver_path = 'chromedriver.exe'
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(0.1)
    return driver

def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

def find_element_with_retries(driver, xpath, retries=1):
    attempt = 0
    while attempt < retries:
        try:
            element = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            scroll_into_view(driver, element)
            return element
        except Exception:
            print(f"Intento {attempt + 1}: No se encontró el elemento, realizando scroll y reintentando...")
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.PAGE_DOWN)
            attempt += 1
    return None

def fetch_html(url):
    """Fetches the HTML content from the given URL using a session."""
    try:
        with requests.Session() as session:
            response = session.get(url)
            response.raise_for_status() 
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None



def main():
    driver = config()
    driver.get('https://pluto.tv')

    on_demand = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/button/span/span')
        )
    )
    on_demand.click()

    select = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div/div/div/main/div[2]/div/div[2]/section/div[3]/div/div[2]/div/div[1]/div/h3')
        )
    )
    select.click()

    results = defaultdict(list)
    current_tematica = None

    for i in range(1, 300):
        xpath = f'//div[@aria-rowindex="{i}"]'
        element_to_click = find_element_with_retries(driver, xpath, retries=3)

        if element_to_click:
            try:
                link_element = element_to_click.find_element(By.TAG_NAME, 'a')
                href_value = link_element.get_attribute('href')
                timeline_links = element_to_click.find_elements(By.CSS_SELECTOR, '.timelines a')
                
                resultado = []
                for index,link in enumerate(timeline_links):
                    href_value2 = link.get_attribute('href')
                    datos = {
                        f"programa {index}": link.text.split('\n'),
                        "link": href_value2
                    }
                    resultado.append(datos)
                    
                href_value = href_value.replace("https://pluto.tv/live-tv/", "https://pluto.tv/latam/live-tv/") + "?lang=en"
                if current_tematica:
                    results[current_tematica].append({
                        'canal':"...",
                        'descripcion': "...",
                        'link': href_value,
                        'programas': resultado
                        })
            except Exception:
                try:
                    h3_element = element_to_click.find_element(By.TAG_NAME, 'h3')
                    h3_value = h3_element.text
                    current_tematica = h3_value
                    results[current_tematica] = []
                except Exception as e:
                    print(f"Error al encontrar <a> o <h3> en aria-rowindex='{i}': {e}")
                    continue
        else:
            print(f"Después de 3 intentos, no se pudo encontrar el elemento con aria-rowindex='{i}'.")
            break

    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'resultados.json')
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)

    driver.quit()

if __name__ == "__main__":
    main()
