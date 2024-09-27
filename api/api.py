# api/api.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import subprocess

# Inicializa o FastAPI
app = FastAPI()

# Ambiente virtual
VENV_PYTHON_PATH = "virtualenv/Scripts/python "

# Diretórios para entrada e saída
INPUT_FILE_PATH = "data/raw_data/input.xlsx"
OUTPUT_FILE_PATH = "data/cleaned_data/output.xlsx"

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    try:
        # Verifica se o arquivo enviado é um Excel
        if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            raise HTTPException(status_code=400, detail="Arquivo inválido. Envie um arquivo Excel (.xlsx).")

        # Cria o diretório se não existir
        #os.makedirs(os.path.dirname(INPUT_FILE_PATH), exist_ok=True)

        # Salva o arquivo recebido em um diretório local
        with open(INPUT_FILE_PATH, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Chama o script main.py para processar o arquivo
        subprocess.run([VENV_PYTHON_PATH, "src/main.py"], check=True)

        # Verifica se o arquivo de saída foi criado
        if not os.path.exists(INPUT_FILE_PATH):
            raise HTTPException(status_code=500, detail="Erro ao processar o arquivo no servidor.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/download/")
async def download():
    # Verifica se o arquivo de saída foi gerado
    if not os.path.exists(OUTPUT_FILE_PATH):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado. Por favor, processe o arquivo primeiro.")

    # Retorna o arquivo processado para download
    return FileResponse(
        OUTPUT_FILE_PATH,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        filename="cleaned_input.xlsx"
    )