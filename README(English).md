# Conecta IFPE Rank-IA

[![pt-BR](https://img.shields.io/badge/lang-pt--BR-green.svg)](README.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](README(English).md)

## About the Project

This repository is part of a larger project. The project documentation is available in the main repository, which can be accessed via this link: https://github.com/Dev-JoseRonaldo/conecta-ifpe

**Conecta IFPE Rank-IA** is an API developed to automate the process of classifying students applying for student assistance scholarships, using artificial intelligence to analyze and score forms based on various socioeconomic criteria.

The system analyzes data from forms submitted in Excel format, processes quantitative and qualitative information (including students' life reports), and generates a classification ordered by level of need, helping educational managers in the fair and efficient distribution of resources.

## Main Features

- **Excel Spreadsheet Processing**: Upload files with candidate data
- **AI Text Analysis**: Natural language processing to evaluate students' life reports
- **Machine Learning Model**: Uses GBM (Gradient Boosting Machine) for candidate classification
- **RESTful API**: Interface for integration with other IFPE systems
- **Automatic Processing**: Transforms input data, performs predictions, and formats results
- **Classification by Need**: Ranks candidates by calculated level of need

## Technologies Used

- **Backend**:
  - Django 5.1.1
  - Django REST Framework 3.15.2
  - Python 3.12.4
  
- **Machine Learning**:
  - scikit-learn
  - spaCy (pt_core_news_lg model for Portuguese)
  - pandas, numpy
  
- **Infrastructure**:
  - Docker and Docker Compose
  - Gunicorn
  
- **Deployment**:
  - Support for Render and Railway platforms

## Project Structure

```
conecta-ifpe-rank-ia/
├── api/                # Django settings
├── rankia/             # Main application
│   ├── src/            # AI processing source code
│   │   ├── main.py     # Main processing flow
│   │   └── utils/      # Helper functions
│   ├── models/         # Trained ML models
│   └── data/           # Data directory
├── manage.py           # Django management script
├── Dockerfile          # Docker configuration
└── requirements.txt    # Project dependencies
```

## How to Run

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/conecta-ifpe-rank-ia.git
   cd conecta-ifpe-rank-ia
   ```

2. Run with Docker Compose:
   ```bash
   docker-compose up
   ```

3. Access the API at: http://localhost:3000

### Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/conecta-ifpe-rank-ia.git
   cd conecta-ifpe-rank-ia
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

5. Access the API at: http://localhost:8000

## API Usage

### Main Endpoint

- **POST /upload/**
  - Receives an Excel file with candidate data
  - Returns JSON with student need ranking

### Request Example

```bash
curl -X POST \
  http://localhost:3000/upload/ \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@path/to/spreadsheet.xlsx'
```
