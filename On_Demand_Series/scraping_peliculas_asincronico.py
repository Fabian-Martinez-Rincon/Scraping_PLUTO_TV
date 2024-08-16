import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup
import os
import re

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
MOVIES_PATH = os.path.join(CURRENT_DIRECTORY, 'Series')

headers = {
    "User-Agent": "python-requests/2.32.3"
}

async def fetch_html(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text()
        else:
            return None
        
async def extract_data(session, link):
    html_content = await fetch_html(session, link)
    if not html_content:
        return None, None, None
    soup = BeautifulSoup(html_content, 'html.parser')
    seccion = soup.find('div', class_='inner')
    descripcion = seccion.find('p')
    descripcion = descripcion.get_text(strip=True) if descripcion else None
    metadatos = seccion.find('ul')
    metadatos = [li.get_text(strip=True) for li in metadatos.findAll('li') if li.get_text(strip=True) and li.get_text(strip=True) != '•'] if metadatos else None
    return descripcion, metadatos

def parse_episode(episode):
    """Parses and returns the information of a single episode."""
    link = episode.find('a').get('href') if episode.find('a') else "No encontrado"
    title = episode.find('h4').get_text(strip=True) if episode.find('h4') else "No encontrado"
    description = episode.find('p', class_="episode-description-atc").get_text(strip=True) if episode.find('p', class_="episode-description-atc") else "No encontrada"
    metadata = episode.find('p', class_="episode-metadata-atc").get_text(strip=True) if episode.find('p', class_="episode-metadata-atc") else "No encontrada"

    return {
        "Titulo": title,
        "Link": link,
        "Descripción": description,
        "Metadata": metadata
    }

async def scrape_series(session, url):
    """Scrapes the series from the given URL and returns a dictionary with episodes organized by season."""
    series_data = {}

    html_content = await fetch_html(session, url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        seccion = soup.find('div', class_='inner')

        # Buscar temporadas
        EXPRESIONES = r'(Temporada|Season|season|temporada) \d+'
        temporadas = [a.get_text(strip=True) for a in seccion.findAll('a') if re.match(EXPRESIONES, a.get_text(strip=True))] if seccion else []

        # Scrape episodios de la primera temporada
        season_number = 1
        series_data[f"Temporada {season_number}"] = [
            parse_episode(episode) for episode in soup.find_all('li', class_='episode-container-atc')
        ]

        # Iterar sobre las temporadas restantes
        for i in range(2, len(temporadas) + 1):
            season_url = f"{url[:-1]}{i}"
            html_content = await fetch_html(session, season_url)
            if html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                season_number += 1
                series_data[f"Temporada {season_number}"] = [
                    parse_episode(episode) for episode in soup.find_all('li', class_='episode-container-atc')
                ]

    return series_data

async def extract_description(session, link):
    descripcion, metadatos = await extract_data(session, link)
    base_link = link.split('/details?lang=en')[0]
    base_link = f"{base_link}/season/1"
    
    temporadas = await scrape_series(session, base_link)
    return descripcion, metadatos, temporadas

async def extract_movies(session, soup):
    movies = []
    start_collecting = False

    for item in soup.find_all('li'):
        link_tag = item.find('a')
        if not link_tag:
            continue
        
        title = link_tag.get('title', link_tag.get_text(strip=True))
        print(f"Procesando la serie: {title}")

        if title == "Series para Maratonear":
            start_collecting = True
            continue

        if start_collecting:
            img_tag = link_tag.find('img')
            if img_tag and 'image' in img_tag['src']:
                link = f"https://pluto.tv{link_tag.get('href')}/details?lang=en"
                description, clasificacion, temporadas = await extract_description(session, link)
                movies.append({
                    'titulo': title,
                    'metadatos': clasificacion,
                    'link': link,
                    'descripcion': description,
                    'temporadas' :temporadas
                    
                })
    
    return movies

async def process_single_category(session, item):
    categoria = item['Categoria']
    url = item['Link']
    html_content = await fetch_html(session, url)

    if not html_content:
        print(f"Error al descargar {categoria}: URL no accesible")
        return None

    print(f"En la categoría '{categoria}'...")
    soup = BeautifulSoup(html_content, 'html.parser')
    movies = await extract_movies(session, soup)

    category_data = {
        "count": len(movies),
        "movies": movies
    }
    
    save_to_json(category_data, f"{categoria.replace(' ', '_').lower()}_movies.json", folder=MOVIES_PATH)
    return categoria

def save_to_json(data, filename, folder='output'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

def combine_json_files(combined_filename):
    combined_data = {}

    for filename in os.listdir(MOVIES_PATH):
        if filename.endswith(".json"):
            filepath = os.path.join(MOVIES_PATH, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                category_name = os.path.splitext(filename)[0]
                combined_data[category_name] = data
    
    combined_filepath = os.path.join(CURRENT_DIRECTORY, combined_filename)
    with open(combined_filepath, "w", encoding="utf-8") as outfile:
        json.dump(combined_data, outfile, ensure_ascii=False, indent=4)

async def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'categories.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        links_json = json.load(json_file)

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [process_single_category(session, item) for item in links_json]
        results = await asyncio.gather(*tasks)
        
        for categoria in results:
            if categoria:
                print(f"Finalizó la categoría '{categoria}'")

    print("Todas las categorías han sido procesadas.")
    
    combine_json_files(combined_filename='combined_series.json')
    print("Todos los archivos JSON han sido combinados en 'combined_series.json'")

if __name__ == "__main__":
    asyncio.run(main())
