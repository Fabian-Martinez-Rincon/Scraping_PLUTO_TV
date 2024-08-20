@echo off
set ENV_NAME=env

:: Crear el entorno virtual
python -m venv %ENV_NAME%

:: Activar el entorno virtual
call %ENV_NAME%\Scripts\activate.bat

:: Instalar dependencias si existe el archivo requirements.txt
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo Archivo requirements.txt no encontrado.
)

:: Ejecutar el archivo principal
python main.py

:: Desactivar el entorno virtual
deactivate

:: Mensaje final
echo Entorno virtual creado e instaladas las dependencias.
