import logging
from scraping_peliculas_series.config.driver import get_driver
from scraping_peliculas_series.scraper import navigate_and_scrape
from scraping_peliculas_series.utils.scraping_utils import save_to_json


from scraping_peliculas_series.configs import CONFIGURATIONS

class ScrapingConfig:
    def __init__(self, config):
        self.on_demand_button = config.get('on_demand_button')
        self.category_button = config.get('category_button')
        self.view_all_button = config.get('view_all_button')
        self.menu_button = config.get('menu_button')
        self.categories_file = config.get('categories_file', 'categories.json')

    def __repr__(self):
        return (
            f"ScrapingConfig("
            f"on_demand_button={self.on_demand_button}, "
            f"category_button={self.category_button}, "
            f"view_all_button={self.view_all_button}, "
            f"menu_button={self.menu_button}, "
            f"categories_file={self.categories_file})"
        )


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

def main():
    """
    Función principal para iniciar el proceso de scraping.
    Itera sobre todas las configuraciones y ejecuta el scraping para cada una.
    """
    for config_name, config_values in CONFIGURATIONS.items():
        scraping_config = ScrapingConfig(config_values)
        print(f"Starting scraping for {config_name} with config: {config_values}")
        start_scraping(scraping_config)

if __name__ == "__main__":
    main()
