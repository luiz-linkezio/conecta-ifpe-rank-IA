# Conecta IFPE Rank-IA

[![pt-BR](https://img.shields.io/badge/lang-pt--BR-green.svg)](README.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](README(English).md)

## Sobre o Projeto

Este repositório é parte de um projeto maior, a documentação do projeto está presente no repositório principal, que pode ser acessado por este link: https://github.com/Dev-JoseRonaldo/conecta-ifpe

O **Conecta IFPE Rank-IA** é uma API desenvolvida para automatizar o processo de classificação de alunos candidatos a bolsas de assistência estudantil, utilizando inteligência artificial para analisar e pontuar formulários com base em diversos critérios socioeconômicos.

O sistema analisa dados de formulários submetidos em formato Excel, processa informações quantitativas e qualitativas (incluindo relatos textuais dos alunos), e gera uma classificação ordenada por nível de necessidade, auxiliando gestores educacionais na distribuição justa e eficiente de recursos.

## Características Principais

- **Processamento de Planilhas Excel**: Upload de arquivos com dados dos candidatos
- **Análise de Texto por IA**: Processamento de linguagem natural para avaliar relatos de vida dos estudantes
- **Modelo de Machine Learning**: Utiliza GBM (Gradient Boosting Machine) para classificação de candidatos
- **API RESTful**: Interface para integração com outros sistemas do IFPE
- **Processamento Automático**: Transforma dados de entrada, realiza predições e formata resultados
- **Classificação por Necessidade**: Ordena candidatos pelo nível de necessidade calculado

## Tecnologias Utilizadas

- **Backend**:
  - Django 5.1.1
  - Django REST Framework 3.15.2
  - Python 3.12.4
  
- **Machine Learning**:
  - scikit-learn
  - spaCy (modelo pt_core_news_lg para português)
  - pandas, numpy
  
- **Infraestrutura**:
  - Docker e Docker Compose
  - Gunicorn
  
- **Implantação**:
  - Suporte para plataformas Render e Railway

## Estrutura do Projeto

```
conecta-ifpe-rank-ia/
├── api/                # Configurações do Django
├── rankia/             # Aplicação principal
│   ├── src/            # Código-fonte do processamento de IA
│   │   ├── main.py     # Fluxo principal de processamento
│   │   └── utils/      # Funções auxiliares
│   ├── models/         # Modelos de ML treinados
│   └── data/           # Diretório para dados
├── manage.py           # Script de gerenciamento Django
├── Dockerfile          # Configuração Docker
└── requirements.txt    # Dependências do projeto
```

## Como Executar

### Usando Docker (Recomendado)

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/conecta-ifpe-rank-ia.git
   cd conecta-ifpe-rank-ia
   ```

2. Execute com Docker Compose:
   ```bash
   docker-compose up
   ```

3. Acesse a API em: http://localhost:3000

### Instalação Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/conecta-ifpe-rank-ia.git
   cd conecta-ifpe-rank-ia
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

5. Acesse a API em: http://localhost:8000

## Uso da API

### Endpoint Principal

- **POST /upload/**
  - Recebe um arquivo Excel com dados dos candidatos
  - Retorna JSON com ranking de necessidade dos alunos

### Exemplo de Requisição

```bash
curl -X POST \
  http://localhost:3000/upload/ \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@caminho/para/planilha.xlsx'
```

