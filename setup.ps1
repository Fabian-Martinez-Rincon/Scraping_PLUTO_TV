# Define el nombre del entorno virtual
$ENV_NAME = "env"

# Crea el entorno virtual usando Python 3
python -m venv $ENV_NAME

# Activa el entorno virtual
. .\$ENV_NAME\Scripts\Activate.ps1

# Verifica si el archivo requirements.txt existe
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
}
else {
    Write-Host "Archivo requirements.txt no encontrado."
}

# Ejecuta el script de Python
python main.py

# Desactiva el entorno virtual
deactivate

Write-Host "Entorno virtual creado e instaladas las dependencias."
