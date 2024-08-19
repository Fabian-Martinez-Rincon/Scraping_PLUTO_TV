import logging
from scraping_peliculas_series.utils.scraping_utils import click_button, click_button_and_get_nav_items

def navigate_and_scrape(driver, config):
    """
    Realiza la navegación y el scraping en el sitio de Pluto TV.
    """
    try:
        click_button(driver, "XPATH", config.on_demand_button)
        click_button(driver, "XPATH", config.category_button)
        click_button(driver, "XPATH", config.view_all_button)
        buttons = click_button_and_get_nav_items(driver, config.menu_button)
        return buttons
    except Exception as e:
        logging.error('An error occurred while scraping: %s', str(e))
        return []
