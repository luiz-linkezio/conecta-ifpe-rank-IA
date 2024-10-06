from rest_framework.views import APIView
from django.http import JsonResponse  # Importa JsonResponse
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
import os
import subprocess

class UploadFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Define o diretório atual como diretório de trabalho
        current_directory = os.path.dirname(os.path.abspath(__file__))
        os.chdir(current_directory)

        # Salva o arquivo temporariamente
        temp_input_path = os.path.join(current_directory, 'data', 'temp', file.name)
        with open(temp_input_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Define o caminho de saída
        temp_output_path = os.path.join(current_directory, 'data', 'temp', 'output.xlsx')
        
        try:
            # Chama o script main.py com subprocess
            """
            venv_python_path = os.path.join(current_directory, '..', 'venv', 'Scripts', 'python.exe')
            subprocess.run([venv_python_path, r'src\main.py', temp_input_path, temp_output_path], check=True)
            """
            subprocess.run(['python3', r'src/main.py', temp_input_path, temp_output_path], check=True)

            # Lê o arquivo de saída processado
            output_df = pd.read_excel(temp_output_path)

            # Remove ou substitui valores NaN
            output_df = output_df.fillna('')  # Substitui NaN por string vazia

            # Converte o DataFrame para uma lista de dicionários
            response_data = output_df.to_dict(orient='records')

            # Limpa arquivos temporários
            os.remove(temp_input_path)
            os.remove(temp_output_path)

            # Retorna um JSON com a resposta
            return JsonResponse({'message': 'File processed successfully', 'data': response_data}, status=status.HTTP_200_OK)
        except subprocess.CalledProcessError as e:
            return JsonResponse({'error': f'Error processing file: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
