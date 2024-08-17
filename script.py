"""
Este módulo ejecuta múltiples scripts de Python relacionados con scraping de películas y series.
Los scripts se ejecutan secuencialmente y se captura el tiempo total de ejecución.
"""

import subprocess
import os
import time

def run_script(script_path):
    """
    Ejecuta un script de Python en la ruta especificada y maneja excepciones si el script falla.
    Args:
    script_path (str): Ruta absoluta al script que se va a ejecutar.
    """
    print(f"Ejecutando el script: {os.path.basename(script_path)}...")
    try:
        subprocess.run(['python', script_path], capture_output=True, text=True, check=True)
        print("Script ejecutado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el script {os.path.basename(script_path)}: {e}")

def main():
    """
    Define el punto de entrada principal del programa, ejecutando varios scripts
    y midiendo el tiempo total de ejecución.
    """
    start_time = time.perf_counter()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    scripts = [
        'On_Demand_Peliculas/scraping_categorias.py',
        'On_Demand_Peliculas/scraping_peliculas_asincronico.py',
        'On_Demand_Series/scraping_categorias.py',
        'On_Demand_Series/scraping_series_asincronico.py',
        'Live_TV/scraping_links.py',
        'Live_TV/scraping.py'
    ]
    scripts = [os.path.join(base_dir, script) for script in scripts]

    for script in scripts:
        run_script(script)

    end_time = time.perf_counter()
    execution_time_minutes = (end_time - start_time) / 60
    print(f"Tiempo total de ejecución: {execution_time_minutes:.2f} minutos")

if __name__ == "__main__":
    main()
