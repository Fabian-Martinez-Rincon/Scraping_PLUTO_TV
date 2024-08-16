from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
from collections import defaultdict

def config():
    driver_path = 'chromedriver.exe'
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(0.5)
    return driver

def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

def find_element_with_retries(driver, xpath, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            element = WebDriverWait(driver, 3).until(
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

def extract_show_details(element):
    try:
        title = element.find_element(By.CLASS_NAME, 'name-item').text
        remaining_time = element.find_element(By.CLASS_NAME, 'remainderTime').text
        description = element.find_element(By.CLASS_NAME, 'description').text
        link = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        return {
            'title': title,
            'remaining_time': remaining_time,
            'description': description,
            'link': link
        }
    except Exception as e:
        print(f"Error extrayendo detalles del show: {e}")
        return None

def main():
    driver = config()
    driver.get('https://pluto.tv')

    # Hacer clic en el botón de On Demand
    on_demand = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/button/span/span')
        )
    )
    on_demand.click()

    # Seleccionar la categoría
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
                show_details = extract_show_details(element_to_click)
                if show_details and current_tematica:
                    results[current_tematica].append(show_details)
            except Exception as e:
                print(f"Error al procesar el elemento en aria-rowindex='{i}': {e}")
                continue  # Ignora este elemento y sigue con el siguiente
        else:
            print(f"Después de 3 intentos, no se pudo encontrar el elemento con aria-rowindex='{i}'.")
            break

    # Guardar los resultados en un archivo JSON
    with open('resultados.json', 'w') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)

    driver.quit()

if __name__ == "__main__":
    main()
