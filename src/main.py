import pandas as pd
import os
from joblib import load
import spacy
from utils.paths import data_path, model_path, scaler_path, one_hoted_columns_list_path, model_text_path
from utils.dataframe_treatment import remove_initial_and_ending_spaces, convert_columns_to_float64, revert_one_hot, filling_missing_columns, reorder_columns, convert_negative_numbers_to_zero, get_invalid_rows, drop_common_rows_from_left_df
from utils.constants import columns_white_list, columns_to_float64, one_hot_encoding_columns
from utils.reading import read_txt_latin1
from utils.ai_processes import ai_process_GBM, ai_process_spacy
from datetime import datetime
import warnings

warnings.filterwarnings('ignore') # Fazendo com que as saídas de alerta sejam ignoradas



# Carrega o arquivo a ser analisado, o modelo que irá analisar, o scaler de normalização e a lista de colunas após o one-hot encoding
def load_data_and_models():
    df = pd.read_excel(data_path)
    model = load(model_path)
    nlp = spacy.load("pt_core_news_lg")
    model_text = load(model_text_path)
    scaler = load(scaler_path)
    one_hoted_columns_list = read_txt_latin1(one_hoted_columns_list_path)

    file_name = os.path.basename(data_path)

    return df, model, scaler, nlp, model_text, one_hoted_columns_list, file_name


# Função responsável por tratar os dados antes da predição do modelo, fazendo com que o dataframe fique no formato de entrada do modelo
def preprocess_dataframe(df, one_hoted_columns_list):
    global resultado_flag

    # Remove espaços em branco nos nomes das colunas
    for col in df.columns:
        df = df.rename({col:remove_initial_and_ending_spaces(col)}, axis='columns')

    # Verifica se o df tem o resultado da escolha da bolsa (PURAMENTE PARA TESTES!!!)
    resultado_flag = False #(PURAMENTE PARA TESTES!!!)
    if "Aluno contemplado com bolsa?" in df.columns: #(PURAMENTE PARA TESTES!!!)
        resultado_flag = True #(PURAMENTE PARA TESTES!!!)

    # Renomeia erro de português em uma das colunas
    if "Condiçõees de moradia familiar" in df:
        df.rename(columns={"Condiçõees de moradia familiar": "Condições de moradia familiar"}, inplace=True)

    # Armazenando a ordem do dataframe antes dos próximos pré-processamentos
    columns_order = df.columns.tolist()

    # Transforma data de nascimento em idade
    df['Data de nascimento'] = (datetime.now() - df['Data de nascimento']).dt.days // 365
    df['Data de nascimento'] = df['Data de nascimento'].astype(float)

    # Converte colunas que tem números em string para float
    df = convert_columns_to_float64(df, columns_to_float64)

    # Armazenando a coluna de aptidão, para testar o desempenho do sistema (DEVE SER REMOVIDO ANTES DE LANÇAR)
    df_aluno_contemplado = df["Aluno contemplado com bolsa?"].copy() # (DEVE SER REMOVIDO ANTES DE LANÇAR)

    # Armazena as colunas que não estão na whitelist de colunas e filtra o df para passar apenas as colunas da whitelist, que serão utilizadas pelo modelo
    df_excluded_columns = df[df.columns.difference(columns_white_list)]
    df = df[columns_white_list]

    # Armazena a coluna do "Relato de vida" e remove esta coluna do dataframe de origem
    df_text_column = df["Relato de vida"]
    df.drop(columns=["Relato de vida"], inplace=True)

    # Armazena linhas com valores inválidos e seus índices, une ela com as colunas faltantes das linhas correspondentes, e dropa estas mesmas linhas no dataframe de colunas excluídas
    invalid_rows = get_invalid_rows(df)
    invalid_rows = invalid_rows.join(df_excluded_columns, how='inner')
    df_excluded_columns.drop(invalid_rows.index, inplace=True)

    # Remove linhas com valores inválidos no dataframe
    df = drop_common_rows_from_left_df(df, invalid_rows)

    # One-hot encoding em determinadas colunas
    df = pd.get_dummies(df, columns=one_hot_encoding_columns, drop_first=False)

    # Preenchendo possíveis colunas faltantes (especialmente as de one-hot encoding que dependem da entrada para existir)
    df = filling_missing_columns(df, one_hoted_columns_list)

    # Ordena os index baseados nas colunas
    df.sort_index(axis=1, inplace=True)

    # Troca valores 'Sim' para True e 'Não' para False, para ser passado no modelo
    df.replace({'Sim': True, 'Não': False}, inplace=True)

    # Transforma valores negativos do dataframe em 0
    df = convert_negative_numbers_to_zero(df)

    return df, df_text_column, invalid_rows, df_excluded_columns, columns_order, df_aluno_contemplado


# 
def midprocess_dataframe(df, text_scores):
    
    df["Relato de vida"] = text_scores

    return df 


# Transforma o dataframe quase no formato original dele, com pouca mudança
def postprocess_dataframe(df, y_pred_proba,invalid_rows, df_excluded_columns, columns_order, file_name, df_text_column):

    # Adiciona uma nova coluna mostrando o nível de necessidade de bolsa de cada aluno
    df['Nível de necessidade'] = y_pred_proba[:, 1]

    # Ordena a coluna a partir do nível de necessidade
    df = df.sort_values(by='Nível de necessidade', ascending=False)

    # Reverte as características que sofreram one-hot encoding
    df = revert_one_hot(df, one_hot_encoding_columns)

    # Ordena os index baseados nas colunas
    df.sort_index(axis=1, inplace=True)

    # Concatena o dataframe com as colunas que foram removidas anteriormente
    df = pd.concat([df, df_excluded_columns], axis=1)

    # Concatena o dataframe com as linhas que foram removidas anteriormente
    df = pd.concat([df, invalid_rows])

    # Dropa a coluna com os scores dos relatos de vida
    df.drop(columns=["Relato de vida"], inplace=True)

    # Concatena o dataframe com os textos de relato de vida originais
    df = pd.concat([df, df_text_column], axis=1)

    # Reordenar colunas para ficar parecido com a entrada
    df = reorder_columns(df, columns_order, resultado_flag) # DEVE SER COLOCADO FALSE ANTES DO LANÇAMENTO!!!

    # Renomeia de volta os valores que eram 'Sim' e 'Não'
    df.replace({True: 'Sim', False: 'Não'}, inplace=True)

    # Renomeando a coluna "Data de nascimento" para "Idade"
    df = df.rename(columns={'Data de nascimento': 'Idade'})

    # Salva a planilha reordenada
    df.to_excel(f'./data/cleaned_data/cleaned_{file_name}', index=False)

    return df


def validate_df(df, df_aluno_contemplado, file_name):
    # dataframe com uma coluna extra de aptidão, para verificar o desempenho do sistema (DEVE SER REMOVIDO ANTES DE LANÇAR)
    df_validation = pd.concat([df, df_aluno_contemplado], axis=1) # (DEVE SER REMOVIDO ANTES DE LANÇAR)

    # Salva a planilha reordenada
    df_validation.to_excel(f'./data/cleaned_data/validation_cleaned_{file_name}', index=False)


def main():
    
    df, model, scaler, nlp, model_text, one_hoted_columns_list, file_name = load_data_and_models() # Carrega os dados, modelo e informações adicionais que serão úteis

    df, df_text_column, invalid_rows, df_excluded_columns, columns_order, df_aluno_contemplado = preprocess_dataframe(df, one_hoted_columns_list) # Transforma o dataframe no quase no formato de entrada do modelo

    text_scores = ai_process_spacy(df_text_column[:len(df)], nlp, model_text) # Transforma a colune de textos em scores para servir de entrada para o modelo
    
    df = midprocess_dataframe(df, text_scores) # Preparações finais para o dataframe estar no formato de entrada do modelo 

    df, y_pred_proba, _ = ai_process_GBM(df, model, scaler) # Normaliza os dados e realiza a predição usando o modelo
    del _

    df = postprocess_dataframe(df, y_pred_proba, invalid_rows, df_excluded_columns, columns_order, file_name, df_text_column) # Transforma o dataframe quase no formato original dele, com pouca mudança

    validate_df(df, df_aluno_contemplado, file_name) # Versão do dataframe com as labels, para realização de testes

if __name__ == "__main__":
    main()