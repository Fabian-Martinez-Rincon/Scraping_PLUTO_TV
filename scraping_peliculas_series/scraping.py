import asyncio
import aiohttp
from bs4 import BeautifulSoup
from scraping_peliculas_series.utils.feth_utils import (
    fetch_html, extract_data, scrape_series
)
from scraping_peliculas_series.utils.utils_json import (
    load_from_json, save_to_json, combine_json_files
)
from scraping_peliculas_series.configs import (
    CONFIGURATIONS_PROCESS, ContentConfig, HEADERS
)

def filter_items(soup, start_marker):
    start_collecting = False

    filtered_items = [
        item for item in soup.find_all('li')
        if (link_tag := item.find('a')) and
           (title := link_tag.get('title', link_tag.get_text(strip=True))) and
           (start_collecting or (start_collecting := title == start_marker)) and
           (img_tag := link_tag.find('img')) and
           'image' in img_tag.get('src', '')
    ]
    return filtered_items

async def extract_movies(session, soup, config, batch_size=20):
    movies = []

    items = filter_items(soup, config.filter)
    items = items[1:]
    print(len(items))

    if len(items) > batch_size:
        batches = [
            items[i:i + batch_size] 
            for i in range(0, len(items), batch_size)
        ]

        tasks = [process_batch(session, batch, config) for batch in batches]
        results = await asyncio.gather(*tasks)

        for result in results:
            movies.extend(result)
    else:
        movies = await process_batch(session, items, config)

    return movies

async def process_batch(session, batch, config):
    batch_movies = []

    for item in batch:
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

        batch_movies.append(movie_data)

    return batch_movies

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

async def scrape_peliculas_series():
    for config_name, config_values in CONFIGURATIONS_PROCESS.items():
        config = ContentConfig(config_values)
        print(f"Procesando {config_name} con configuración: {config.read_file}")
        links_json = load_from_json(config.read_file)

        async with aiohttp.ClientSession(headers=HEADERS) as session:
            tasks = [
                process_single_category(session, item, config, config_name)
                for item in links_json
            ]
            results = await asyncio.gather(*tasks)
            for categoria in results:
                if categoria:
                    print(f"Finalizó la categoría '{categoria}'")

        combine_json_files(config_name, f'{config_name}.json', 'resultados')

async def main():
    for config_name, config_values in CONFIGURATIONS_PROCESS.items():
        config = ContentConfig(config_values)
        print(f"Procesando {config_name} con configuración: {config.read_file}")
        links_json = load_from_json(config.read_file)

        async with aiohttp.ClientSession(headers=HEADERS) as session:
            tasks = [
                process_single_category(session, item, config, config_name)
                for item in links_json
            ]
            results = await asyncio.gather(*tasks)
            for categoria in results:
                if categoria:
                    print(f"Finalizó la categoría '{categoria}'")

        combine_json_files(config_name, f'{config_name}.json', 'resultado')

if __name__ == "__main__":
    asyncio.run(main())
