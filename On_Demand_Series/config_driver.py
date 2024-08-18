from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def config():
    """
    Configura y retorna un driver de Selenium para Chrome con opciones específicas.

    Configura el navegador para abrirse en modo incógnito y maximizado.

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