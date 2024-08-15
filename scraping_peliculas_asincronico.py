import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup
import os

async def fetch_html(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Error al acceder a {url}: Estado {response.status}")
                return None
    except aiohttp.ClientError as e:
        print(f"Error en la solicitud de {url}: {str(e)}")
        return None

async def extract_description(session, link):
    html_content = await fetch_html(session, link)
    if not html_content:
        return None, None
    soup = BeautifulSoup(html_content, 'html.parser')
    seccion = soup.find('div', class_='inner')
    if not seccion:
        return None, None
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

    if category_data["count"] > 0:  # Solo guarda si hay películas
        save_to_json(category_data, f"{categoria.replace(' ', '_').lower()}_movies.json")
    
    return categoria

def save_to_json(data, filename, folder='output'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

async def main():
    with open('categories.json', 'r', encoding='utf-8') as json_file:
        links_json = json.load(json_file)

    async with aiohttp.ClientSession() as session:
        tasks = [process_single_category(session, item) for item in links_json]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                print(f"Error: {result}")
            elif result:
                print(f"Finalizó la categoría '{result}'")

    print("Todas las categorías han sido procesadas.")

if __name__ == "__main__":
    asyncio.run(main())
