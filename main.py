import asyncio
from scraping_peliculas_series.main import scrape_category_peliculas_series
from scraping_peliculas_series.scraping import scrape_peliculas_series

def main():
    #print("Iniciando scraping de canales...")
    #scrape_canales()  # Ejecuta el script para scraping de canales

    print("Iniciando scraping de películas y series...")
    scrape_category_peliculas_series()  # Ejecuta el script para scraping de películas y series
    asyncio.run(scrape_peliculas_series())  # Ejecuta el script para scraping de películas y series

    print("Proceso completado.")

if __name__ == "__main__":
    main()
