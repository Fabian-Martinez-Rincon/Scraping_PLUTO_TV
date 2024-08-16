from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
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
    
    # Clic en el botón de On Demand (o similar)
    on_demand = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/button/span/span')
        )
    )
    on_demand.click()

    # Clic en el elemento especificado
    select = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div/div/div/main/div[2]/div/div[2]/section/div[3]/div/div[2]/div/div[1]/div/h3')
        )
    )
    select.click()

    body = driver.find_element(By.TAG_NAME, 'body')
    
    # Lista para almacenar los elementos encontrados
    all_channels = []

    # Realizar scroll y capturar elementos en cada iteración
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Obtener la fuente de la página y analizarla
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Buscar y capturar los elementos deseados
        channels = soup.find_all('div', class_='channelListItem-0-2-313 channel')
        
        for channel in channels:
            channel_name = channel.find('div', {'role': 'rowheader'}).get_text(strip=True)
            image_div = channel.find('div', class_='image')
            image_style = image_div.get('style')
            image_url = image_style.split("url(\"")[1].split("\")")[0] if image_style else None
            
            all_channels.append({
                'name': channel_name,
                'image_url': image_url
            })

        # Realizar scroll hacia abajo
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        
        # Calcular la nueva altura de la página después del scroll
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Si la altura de la página no cambia, significa que hemos llegado al final
        if new_height == last_height:
            break

        last_height = new_height

    # Cerrar el WebDriver
    driver.quit()

    # Imprimir los elementos capturados
    for channel in all_channels:
        print(f"Nombre del canal: {channel['name']}")
        print(f"URL de la imagen: {channel['image_url']}")
        print("------")

if __name__ == "__main__":
    main()
