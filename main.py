import asyncio
from scraping_peliculas_series.main import scrape_category_peliculas_series
from scraping_peliculas_series.scraping import scrape_peliculas_series
from scraping_canales.scraping_links import scrape_canales
from scraping_canales.scraping import scrape_data_canales


def main():
    print("Iniciando scraping de canales...")
    scrape_canales()
    asyncio.run(scrape_data_canales())
    print("Iniciando scraping de películas y series...")
    scrape_category_peliculas_series()
    asyncio.run(scrape_peliculas_series())
    print("Proceso completado.")

if __name__ == "__main__":
    main()
