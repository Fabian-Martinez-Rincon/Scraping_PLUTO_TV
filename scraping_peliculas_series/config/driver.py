from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_driver():
    """
    Configura y retorna un driver de Selenium para Chrome con opciones específicas.

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
