import logging
from scraping_peliculas_series.config.driver import get_driver
from scraping_peliculas_series.scraper import navigate_and_scrape
from scraping_peliculas_series.utils.utils_json import save_to_json
from scraping_peliculas_series.configs import CONFIGURATIONS_BUTTONS, ScrapingConfig

def start_scraping(scraping_config):
    """
    Inicializa el WebDriver de Selenium, realiza el scraping,
    y guarda los datos en un archivo JSON.
    """
    driver = None
    try:
        driver = get_driver()
        driver.get('https://pluto.tv')
        buttons = navigate_and_scrape(driver, scraping_config)
        if buttons:
            save_to_json(buttons, scraping_config.categories_file)
        else:
            logging.warning("No data was scraped.")
    except Exception as e:
        logging.error("An error occurred during the scraping process: %s", str(e))
    finally:
        if driver:
            driver.quit()

def scrape_category_peliculas_series():
    """
    Función principal para iniciar el proceso de scraping.
    Itera sobre todas las configuraciones y ejecuta el scraping para cada una.
    """
    for config_name, config_values in CONFIGURATIONS_BUTTONS.items():
        scraping_config = ScrapingConfig(config_values)
        print(f"Starting scraping for {config_name} with config: {config_values}")
        start_scraping(scraping_config)

def main():
    """
    Función principal para iniciar el proceso de scraping.
    Itera sobre todas las configuraciones y ejecuta el scraping para cada una.
    """
    for config_name, config_values in CONFIGURATIONS_BUTTONS.items():
        scraping_config = ScrapingConfig(config_values)
        print(f"Starting scraping for {config_name} with config: {config_values}")
        start_scraping(scraping_config)

if __name__ == "__main__":
    main()
    