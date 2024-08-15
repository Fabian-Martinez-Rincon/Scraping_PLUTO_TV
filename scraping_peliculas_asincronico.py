import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup
import os

headers = {
    "User-Agent": "python-requests/2.32.3"
}

async def fetch_html(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text()
        else:
            return None

async def extract_description(session, link):
    html_content = await fetch_html(session, link)
    if not html_content:
        return None, None
    soup = BeautifulSoup(html_content, 'html.parser')
    seccion = soup.find('div', class_='inner')
    descripcion = seccion.find('p')
    descripcion = descripcion.get_text(strip=True) if descripcion else None
    metadatos = seccion.find('ul')
    metadatos = [li.get_text(strip=True) for li in metadatos.findAll('li') if li.get_text(strip=True) and li.get_text(strip=True) != '•'] if metadatos else None
    
    return descripcion, metadatos

async def extract_movies(session, soup):
    movies = []
    start_collecting = False

    for item in soup.find_all('li'):
        link_tag = item.find('a')
        if not link_tag:
            continue
        
        title = link_tag.get('title', link_tag.get_text(strip=True))
        print(f"Procesando la pelicula: {title}")

        if title == "Invierno de Película":
            start_collecting = True
            continue

        if start_collecting:
            img_tag = link_tag.find('img')
            if img_tag and 'image' in img_tag['src']:
                link = f"https://pluto.tv{link_tag.get('href')}/details?lang=en"
                description, clasificacion = await extract_description(session, link)
                movies.append({
                    'titulo': title,
                    'metadatos': clasificacion,
                    'link': link,
                    'descripcion': description
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

    save_to_json(category_data, f"{categoria.replace(' ', '_').lower()}_movies.json")
    return categoria

def save_to_json(data, filename, folder='output'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

def combine_json_files(output_folder, combined_filename):
    combined_data = {}
    for filename in os.listdir(output_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(output_folder, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                category_name = os.path.splitext(filename)[0]
                combined_data[category_name] = data
    
    # Guardar el JSON combinado en un solo archivo
    combined_filepath = os.path.join(output_folder, combined_filename)
    with open(combined_filepath, "w", encoding="utf-8") as outfile:
        json.dump(combined_data, outfile, ensure_ascii=False, indent=4)

async def main():
    with open('categories.json', 'r', encoding='utf-8') as json_file:
        links_json = json.load(json_file)

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [process_single_category(session, item) for item in links_json]
        results = await asyncio.gather(*tasks)
        
        for categoria in results:
            if categoria:
                print(f"Finalizó la categoría '{categoria}'")

    print("Todas las categorías han sido procesadas.")
    
    combine_json_files(output_folder='output', combined_filename='combined_movies.json')
    print("Todos los archivos JSON han sido combinados en 'combined_movies.json'")

if __name__ == "__main__":
    asyncio.run(main())
