# Configuración de las cabeceras HTTP
HEADERS = {
    "User-Agent": "python-requests/2.32.3"
}

# Configuración del scraping
class ScrapingConfig:
    """
    A configuration class for managing the scraping settings.

    Attributes:
        on_demand_button (str): XPath for the "On Demand" button.
        category_button (str): XPath for the category button.
        view_all_button (str): XPath for the "View All" button.
        menu_button (str): XPath for the navigation menu button.
        categories_file (str): JSON file to save the scraped categories.
    """
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

# Configuración del contenido
class ContentConfig:
    """
    A configuration class for managing content scraping settings.

    Attributes:
        filter (str): The filter to start scraping from a specific section.
        include_temporadas (bool): Whether to include seasons in the scraping.
        read_file (str): The JSON file to read the categories from.
    """
    def __init__(self, config):
        self.filter = config.get('filter')
        self.include_temporadas = config.get('include_temporadas', False)
        self.read_file = config.get('read_file', 'categories_series.json')

    def __repr__(self):
        return (
            f"ContentConfig("
            f"filter={self.filter}, "
            f"include_temporadas={self.include_temporadas}, "
            f"read_file={self.read_file})"
        )

CONFIGURATIONS_BUTTONS = {
    'series': {
        'on_demand_button': "//nav/span[2]/a/span",
        'category_button': "//span[text()='Series']",
        'view_all_button': "//section[3]/span/div/div[1]/span/a",
        'menu_button': "//div[1]/div/div[1]/div/button",
        'categories_file': "categories_series.json",
    },
    'peliculas' : {
        'on_demand_button': "//nav/span[2]/a/span",
        'category_button': "//span[text()='Películas']",
        'view_all_button': "//section[3]/span/div/div[1]/span/a",
        'menu_button': "//div[1]/div/div[1]/div/button",
        'categories_file': "categories_peliculas.json",
    }
}

CONFIGURATIONS_PROCESS = {
    'series': {
        'filter': "Series para Maratonear",
        'include_temporadas': True,
        'read_file': "categories_series.json"
    },
    'peliculas' : {
        'filter': "Invierno de Película",
        'include_temporadas': False,
        'read_file': "categories_peliculas.json"
    }
}
