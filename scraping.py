import os
import json
import asyncio
import aiohttp

from bs4 import BeautifulSoup
from scraping_peliculas_series.utils.feth_utils import (
    fetch_html, extract_data, scrape_series
)
from scraping_peliculas_series.utils.scraping_utils import save_to_json, combine_json_files

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

headers = {
    "User-Agent": "python-requests/2.32.3"
}

class ContentConfig:
    def __init__(self, config):
        self.filter = config.get('filter')
        self.include_temporadas = config.get('include_temporadas', False)
        self.read_file = config.get('read_file', 'categories_series.json')

    def __repr__(self):
        return (
            f"ContentConfig("
            f"filter={self.filter}, "
            f"include_temporadas={self.include_temporadas})"
            f"read_file={self.read_file})"
        )


CONFIGURATIONS = {
    'Series': {
        'filter': "Series para Maratonear",
        'include_temporadas': True,
        'read_file': "categories_series.json"
    },
    'Peliculas': {
        'filter': "Invierno de Película",
        'include_temporadas': False,
        'read_file': "categories_peliculas.json"
    }
}

def filter_items(soup, start_marker):
    start_collecting = False

    # Filtra los elementos que tienen un enlace (<a>) y que aparecen después del marcador
    filtered_items = [
        item for item in soup.find_all('li')
        if (link_tag := item.find('a')) and
           (title := link_tag.get('title', link_tag.get_text(strip=True))) and
           (start_collecting or (start_collecting := title == start_marker)) and
           (img_tag := link_tag.find('img')) and
           'image' in img_tag.get('src', '')
    ]
    return filtered_items

async def extract_movies(session, soup, config):
    movies = []

    # Filtra los elementos que tienen un enlace (<a>) y que aparecen después del marcador
    items = filter_items(soup, config.filter)

    # Procesa los elementos filtrados
    for item in items[1:]:
        link_tag = item.find('a')
        title = link_tag.get('title', link_tag.get_text(strip=True))
        link = f"https://pluto.tv{link_tag.get('href')}/details?lang=en"
        descripcion, metadatos = await extract_data(session, link)

        movie_data = {
            'titulo': title,
            'metadatos': metadatos,
            'link': link,
            'descripcion': descripcion
        }

        if config.include_temporadas:
            base_link = f"https://pluto.tv{link_tag.get('href')}/season/1"
            temporadas = await scrape_series(session, base_link)
            movie_data['temporadas'] = temporadas

        movies.append(movie_data)
    return movies


async def process_single_category(session, item, config, folder_name='Series'):
    categoria = item['Categoria']
    url = item['Link']
    html_content = await fetch_html(session, url)

    if not html_content:
        print(f"Error al descargar {categoria}: URL no accesible")
        return None

    soup = BeautifulSoup(html_content, 'html.parser')
    movies = await extract_movies(session, soup, config)

    category_data = {
        "count": len(movies),
        "movies": movies
    }
    save_to_json(category_data, f"{categoria.replace(' ', '_').lower()}_movies.json", folder_name)
    return categoria

async def main():
    for config_name, config_values in CONFIGURATIONS.items():
        config = ContentConfig(config_values)

        print(f"Procesando {config_name} con configuración: {config}")

        file_path = os.path.join(CURRENT_DIRECTORY, config.read_file)
        with open(file_path, 'r', encoding='utf-8') as json_file:
            links_json = json.load(json_file)

        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = [
                process_single_category(session, item, config, config_name)
                for item in links_json
            ]
            results = await asyncio.gather(*tasks)
            for categoria in results:
                if categoria:
                    print(f"Finalizó la categoría '{categoria}'")

        print("Todas las categorías han sido procesadas.")
        combine_json_files(config_name, f'{config_name}.json', 'Resultado')
        print("Todos los archivos JSON han sido combinados en 'combined_series.json'")

if __name__ == "__main__":
    asyncio.run(main())
