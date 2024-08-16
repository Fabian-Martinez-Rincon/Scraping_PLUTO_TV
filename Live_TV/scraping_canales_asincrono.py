import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
from collections import defaultdict
import aiohttp
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "python-requests/2.32.3"
}

def config():
    driver_path = 'chromedriver.exe'
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    return driver

def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

async def fetch_html(session, url):
    """Fetches the HTML content from the given URL using aiohttp session."""
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Error fetching {url}: {e}")
        return None

async def find_element_with_retries(driver, xpath, retries=3):
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
            await asyncio.sleep(2)  # Espera a que el contenido cargue después del scroll
            attempt += 1
    return None

async def process_element(driver, i, session, results, current_tematica):
    xpath = f'//div[@aria-rowindex="{i}"]'
    element_to_click = await find_element_with_retries(driver, xpath)

    if element_to_click:
        try:
            link_element = element_to_click.find_element(By.TAG_NAME, 'a')
            href_value = link_element.get_attribute('href')
            print(f"Valor del atributo href del elemento {i}: {href_value}")
            modified_link = href_value.replace("https://pluto.tv/live-tv/", "https://pluto.tv/latam/live-tv/").replace("/details", "/details?lang=en")
            html_content = await fetch_html(session, modified_link)
            if html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                seccion = soup.find('div', class_="inner")
                titulo = seccion.find('h2').get_text(strip=True) if seccion.find('h2') else "No encontrado"
                descripcion = seccion.find('p').get_text(strip=True) if seccion.find('p') else "No encontrada"
                if current_tematica:
                    results[current_tematica].append({
                        'canal': titulo,
                        'link': href_value,
                        'descripcion': descripcion
                    })
        except Exception:
            try:
                # Si no encuentra el <a>, busca el <h3>
                h3_element = element_to_click.find_element(By.TAG_NAME, 'h3')
                h3_value = h3_element.text
                print(f"Valor del texto <h3> del elemento {i}: {h3_value}")
                return h3_value
            except Exception as e:
                print(f"Error al encontrar <a> o <h3> en aria-rowindex='{i}': {e}")
    else:
        print(f"Después de 3 intentos, no se pudo encontrar el elemento con aria-rowindex='{i}'.")

    return current_tematica

async def main():
    driver = config()
    driver.get('https://pluto.tv')
    await asyncio.sleep(5)

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

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 200):
            tasks.append(process_element(driver, i, session, results, current_tematica))

        # Wait for all tasks to complete
        tematicas = await asyncio.gather(*tasks)

        for tematica in tematicas:
            if tematica:
                current_tematica = tematica
                results[current_tematica] = []

    # Guardar los resultados en un archivo JSON
    with open('resultados.json', 'w') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)

    driver.quit()

if __name__ == "__main__":
    asyncio.run(main())
