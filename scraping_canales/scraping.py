import asyncio
import aiohttp
from scraping_peliculas_series.utils.feth_utils import (
    estract_section
)
from scraping_peliculas_series.utils.utils_json import (
    load_from_json, save_to_json
)
from scraping_peliculas_series.configs import HEADERS

async def process_data(session, data):
    """Processes the data, scrapes information from channels, and updates the data structure."""
    tasks = []

    for key in data.keys():
        for item in data[key]:
            original_link = item['link']
            print(f'link = "{original_link}"')
            tasks.append(estract_section(session, original_link))

    print('Esperando a que todas las tareas se completen...')
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print('Todas las tareas completadas o con errores capturados.')

    index = 0
    for key in data.keys():
        for item in data[key]:
            result = results[index]
            if isinstance(result, Exception):
                print(f"Error processing {item['link']}: {result}")
                titulo, descripcion = "Error encontrado", "Descripción no disponible"
            else:
                titulo, descripcion = result
            item['canal'] = titulo
            item['descripcion'] = descripcion
            index += 1
    return data

async def main():
    data = load_from_json('resultados.json')

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        updated_data = await process_data(session, data)

    save_to_json(updated_data, 'resultados_actualizados.json')

if __name__ == "__main__":
    asyncio.run(main())
