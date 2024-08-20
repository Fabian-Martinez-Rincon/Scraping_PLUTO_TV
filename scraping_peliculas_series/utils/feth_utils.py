import logging
import asyncio
import re
import aiohttp

from bs4 import BeautifulSoup

async def fetch_html(session, url, timeout=10):
    """
    Fetches HTML content from a given URL using the provided session.

    Args:
        session (aiohttp.ClientSession): The session to use for the HTTP request.
        url (str): The URL to fetch.
        timeout (int): The maximum time to wait for a response.

    Returns:
        str or None: The HTML content if successful, None otherwise.
    """
    try:
        async with session.get(url, timeout=timeout) as response:
            if response.status == 200:
                #logging.info("Successfully fetched %s", url)
                return await response.text()
            else:
                logging.warning("Failed to fetch %s with status %d", url, response.status)
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logging.error("Error fetching %s: %s", url, str(e))
    return None

async def extract_data(session, link):
    """
    Fetches HTML content and extracts description and metadata from a given link.

    Args:
        session (aiohttp.ClientSession): The session to use for the HTTP request.
        link (str): The URL to fetch and extract data from.

    Returns:
        tuple: A tuple containing the description (str) and metadata (list) 
        if successful, otherwise (None, None).
    """
    html_content = await fetch_html(session, link)
    if not html_content:
        return None, None

    soup = BeautifulSoup(html_content, 'html.parser')
    seccion = soup.find('div', class_='inner')

    if not seccion:
        logging.warning("No se encontró la sección esperada en %s", link)
        return None, None

    # Extract the description
    descripcion = seccion.find('p')
    descripcion = descripcion.get_text(strip=True) if descripcion else None

    # Extract the metadata
    metadatos = seccion.find('ul')
    if metadatos:
        metadatos = [
            li.get_text(strip=True)
            for li in metadatos.find_all('li')
            if li.get_text(strip=True) and li.get_text(strip=True) != '•'
        ]
    else:
        metadatos = None

    return descripcion, metadatos

def extract_data_episode(episode):
    """
    Parses and returns the information of a single episode.

    Args:
        episode (bs4.element.Tag): The BeautifulSoup tag containing the episode data.

    Returns:
        dict: A dictionary with the episode's title, link, description, and metadata.
    """
    def get_text_or_default(element, selector, default="No encontrado", class_name=None):
        tag = element.find(selector, class_=class_name) if class_name else element.find(selector)
        return tag.get_text(strip=True) if tag else default

    link = episode.find('a').get('href', "No encontrado") if episode.find('a') else "No encontrado"
    section = episode.find('section')
    title = get_text_or_default(
        section,
        'h4',
        "No encontrado")
    description = get_text_or_default(
        section,
        'p', 
        "No encontrada",
        class_name="episode-description-atc")
    metadata = get_text_or_default(section, 'p', "No encontrada", class_name="episode-metadata-atc")

    return {
        "Titulo": title,
        "Link": link,
        "Descripción": description,
        "Metadata": metadata
    }

async def scrape_series(session, url):
    """
    Scrapes the series from the given URL and returns a dictionary with episodes organized by season

    Args:
        session (aiohttp.ClientSession): The session to use for the HTTP requests.
        url (str): The URL of the series page to scrape.

    Returns:
        dict: A dictionary where keys are season names and values are lists of episode data.
    """
    series_data = {}

    html_content = await fetch_html(session, url)
    if not html_content:
        return series_data

    soup = BeautifulSoup(html_content, 'html.parser')
    seccion = soup.find('div', class_='inner')

    if not seccion:
        return series_data

    season_links = get_season_links(seccion)
    print(len(season_links))
    if len(season_links) <= 1:
        series_data["Temporada 1"] = parse_episodes(soup)
        return series_data

    tasks = [
        scrape_season(session, url, season_number)
        for season_number in
        range(1, len(season_links) + 1)
    ]
    seasons_data = await asyncio.gather(*tasks)

    for season_number, episodes in enumerate(seasons_data, start=1):
        series_data[f"Temporada {season_number}"] = episodes

    return series_data

def get_season_links(section):
    """
    Extracts the links or labels for all seasons available in the section.

    Args:
        section (bs4.element.Tag): The section containing season links.

    Returns:
        list: A list of season names or numbers.
    """
    season_pattern = r'(Temporada|Season|season|temporada) \d+'
    return [
        a.get_text(strip=True)
        for a in section.findAll('a')
        if re.match(season_pattern, a.get_text(strip=True))
    ]

async def scrape_season(session, base_url, season_number):
    """
    Scrapes episodes from a specific season.

    Args:
        session (aiohttp.ClientSession): The session to use for the HTTP request.
        base_url (str): The base URL of the series.
        season_number (int): The season number to scrape.

    Returns:
        list: A list of episode data for the specified season.
    """
    season_url = f"{base_url[:-1]}{season_number}"
    html_content = await fetch_html(session, season_url)

    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    return [
        extract_data_episode(episode)
        for episode in soup.find_all('li', class_='episode-container-atc')
    ]

def parse_episodes(soup):
    """
    Extracts episode data from the given soup object.

    Args:
        soup (bs4.BeautifulSoup): The BeautifulSoup object containing episode data.

    Returns:
        list: A list of dictionaries containing episode data.
    """
    return [
        extract_data_episode(episode)
        for episode in soup.find_all('li', class_='episode-container-atc')
    ]


async def estract_section(session, url: str):
    """Scrapes the series from the given URL and returns the title and description."""
    try:
        html_content = await fetch_html(session, url)
        if not html_content:
            return "No encontrado", "No encontrada"

        soup = BeautifulSoup(html_content, 'html.parser')
        seccion = soup.find('div', class_="inner")

        if seccion:
            titulo_element = seccion.find('h2')
            descripcion_element = seccion.find('p')

            titulo = titulo_element.get_text(strip=True) if titulo_element else "No encontrado"
            descripcion = descripcion_element.get_text(strip=True) if descripcion_element else "No encontrada"
        else:
            titulo, descripcion = "No encontrado", "No encontrada"
        return titulo, descripcion

    except Exception as e:
        print(f"Error al extraer la sección: {e}")
        return "Error", "Error"