$ENV_NAME = "env"

python -m venv $ENV_NAME

. .\$ENV_NAME\Scripts\Activate.ps1

if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
}
else {
    Write-Host "Archivo requirements.txt no encontrado."
}

python main.py
deactivate

Write-Host "Entorno virtual creado e instaladas las dependencias."