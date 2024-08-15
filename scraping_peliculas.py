import requests
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

def fetch_html(url):
    with requests.Session() as session:
        response = session.get(url)
        return response.text if response.status_code == 200 else None

def extract_description(link):
    html_content = fetch_html(link)
    if not html_content:
        return None
    soup = BeautifulSoup(html_content, 'html.parser')
    seccion = soup.find('div', class_='inner')
    descripcion = seccion.find('p')
    descripcion = descripcion.get_text(strip=True) if descripcion else None
    metadatos = seccion.find('ul')
    metadatos = [li.get_text(strip=True) for li in metadatos.findAll('li') if li.get_text(strip=True) and li.get_text(strip=True) != '•'] if metadatos else None
    
    return descripcion, metadatos

def extract_movies(soup):
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
                description, clasificacion = extract_description(link)
                movies.append({
                    'titulo': title,
                    'metadatos': clasificacion,
                    'link': link,
                    'descripcion': description
                })
    
    return movies

def process_single_category(item):
    categoria = item['Categoria']
    url = item['Link']
    html_content = fetch_html(url)

    if not html_content:
        print(f"Error al descargar {categoria}: URL no accesible")
        return None

    print(f"En la categoría '{categoria}'...")
    soup = BeautifulSoup(html_content, 'html.parser')
    movies = extract_movies(soup)

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

def main():
    with open('categories.json', 'r', encoding='utf-8') as json_file:
        links_json = json.load(json_file)

    with ThreadPoolExecutor(max_workers=8) as executor:  # Puedes ajustar el número de workers
        futures = [executor.submit(process_single_category, item) for item in links_json]
        
        for future in as_completed(futures):
            categoria = future.result()
            if categoria:
                print(f"Finalizó la categoría '{categoria}'")

    print("Todas las categorías han sido procesadas.")

if __name__ == "__main__":
    main()
