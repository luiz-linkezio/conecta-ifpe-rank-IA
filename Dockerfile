# Use a imagem base do Python
FROM python:3.12.4

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Atualiza o pip e instala os pacotes do Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY . .

# Expõe a porta que o Django está usando
EXPOSE 3000

# Comando para iniciar sua aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
