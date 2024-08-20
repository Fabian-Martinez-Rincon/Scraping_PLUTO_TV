import asyncio
import time
import os
from scraping_peliculas_series.main import scrape_category_peliculas_series
from scraping_peliculas_series.scraping import scrape_peliculas_series
from scraping_canales.scraping_links import scrape_canales
from scraping_canales.scraping import scrape_data_canales


async def run_scraping_tasks():
    loop = asyncio.get_running_loop()
    scrape_canales_task = loop.run_in_executor(None, scrape_canales)

    await asyncio.gather(
        scrape_canales_task,
        scrape_peliculas_series()
    )

def main():
    start_time = time.time()

    print("Iniciando scraping de películas y series...")
    scrape_category_peliculas_series()

    print("Iniciando scraping de canales y películas/series en paralelo...")
    asyncio.run(run_scraping_tasks())

    asyncio.run(scrape_data_canales())

    end_time = time.time()

    execution_time = end_time - start_time

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Proceso completado en {execution_time:.2f} segundos.")

if __name__ == "__main__":
    main()
