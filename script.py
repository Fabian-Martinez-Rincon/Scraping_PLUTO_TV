import subprocess
import os
import time

start_time = time.perf_counter()

base_dir = os.path.dirname(os.path.abspath(__file__))

# Rutas de los scripts que quieres ejecutar
script1 = os.path.join(base_dir, 'On_Demand_Peliculas', 'scraping_categorias.py')
script2 = os.path.join(base_dir, 'On_Demand_Peliculas', 'scraping_peliculas_asincronico.py')
script3 = os.path.join(base_dir, 'On_Demand_Series', 'scraping_categorias.py')
script4 = os.path.join(base_dir, 'On_Demand_Series', 'scraping_peliculas_asincronico.py')

# Ejecutar el primer script
# print("Ejecutando el primer script...")
# subprocess.run(['python', script1], capture_output=True, text=True)
# print("Primer script terminado.")

# # Ejecutar el segundo script
# print("Ejecutando el segundo script...")
# subprocess.run(['python', script2], capture_output=True, text=True)
# print("Segundo script terminado.")

print("Ejecutando el tercero script...")
subprocess.run(['python', script3], capture_output=True, text=True)
print("Segundo script terminado.")

print("Ejecutando el cuarto script...")
subprocess.run(['python', script4], capture_output=True, text=True)
print("Segundo script terminado.")

# Marca el final del tiempo
end_time = time.perf_counter()

# Calcula el tiempo de ejecución en minutos
execution_time_minutes = (end_time - start_time) / 60
print(f"Tiempo total de ejecución: {execution_time_minutes:.2f} minutos")
