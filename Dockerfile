# Use a imagem base do Python
FROM python:3.12.4

# Instala Node.js
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY rank-ia/requirements.txt .

# Atualiza o pip e instala virtualenv
RUN pip install --upgrade pip

# Instala os pacotes do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY . .

# Muda para o diretório da API e instala as dependências do Node.js
WORKDIR /app/api

RUN npm install

# Comando para iniciar sua aplicação (Node.js neste caso)
CMD ["npm", "run", "start"]
