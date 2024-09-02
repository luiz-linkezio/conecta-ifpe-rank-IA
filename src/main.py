import pandas as pd
import os
from joblib import load
from utils.paths import data_path, model_path, scaler_path, one_hoted_columns_list_path
from utils.dataframe_treatment import remove_initial_and_ending_spaces, convert_columns_to_float64, revert_one_hot, filling_missing_columns, reorder_columns, convert_negative_numbers_to_zero
from utils.constants import columns_white_list, columns_to_float64, one_hot_encoding_columns
from utils.reading import read_txt_latin1
from datetime import datetime
import warnings

warnings.filterwarnings('ignore') # Fazendo com que as saídas de alerta sejam ignoradas



# Carrega o arquivo a ser analisado, o modelo que irá analisar, o scaler de normalização e a lista de colunas após o one-hot encoding
def load_data_and_models(data_path, model_path, scaler_path, one_hoted_columns_list_path):
    df = pd.read_excel(data_path)
    model = load(model_path)
    scaler = load(scaler_path)
    one_hoted_columns_list = read_txt_latin1(one_hoted_columns_list_path)

    file_name = os.path.basename(data_path)

    return df, model, scaler, one_hoted_columns_list, file_name


# Função responsável por tratar os dados antes da predição do modelo
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

    # Armazenando a ordem do dataframe antes dos próximos preprocessamentos
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

    # Remove a coluna Relato de Vida (TEMPORÁRIO)
    df = df.drop(columns=["Relato de vida"]) # (TEMPORÁRIO)

    # Armazena linhas com valores nulos e seus índices, une ela com as colunas faltantes das linhas correspondentes, e dropa estas mesmas linhas no dataframe de colunas excluídas
    rows_with_na = df[df.isna().any(axis=1)]
    rows_with_na = rows_with_na.join(df_excluded_columns, how='inner')
    df_excluded_columns = df_excluded_columns.drop(rows_with_na.index)

    # Remove linhas com valores nulos no dataframe
    df = df.dropna(axis=0)

    # One-hot encoding
    df = pd.get_dummies(df, columns=one_hot_encoding_columns, drop_first=False)

    # Preenchendo possíveis colunas faltantes (especialmente as de one-hot encoding que dependem da entrada para existir)
    df = filling_missing_columns(df, one_hoted_columns_list)

    # Ordena os index baseados nas colunas
    df.sort_index(axis=1, inplace=True)

    # Troca valores 'Sim' para True e 'Não' para False, para ser passado no modelo
    df.replace({'Sim': True, 'Não': False}, inplace=True)

    # Transforma valores negativos do dataframe em 0
    df = convert_negative_numbers_to_zero(df)

    return df, rows_with_na, df_excluded_columns, columns_order, df_aluno_contemplado


# Função responsável por normalizar os dados, fazer a predição do modelo e fazer tratamentos finais
def postprocess_dataframe(df, model, scaler, rows_with_na, df_excluded_columns, columns_order, file_name):

    # Normaliza os dados
    X = scaler.transform(df)

    # Modelo gera um score do quanto o aluno precisa da bolsa
    y_pred_proba = model.predict_proba(X)

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
    df = pd.concat([df, rows_with_na])

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
    
    df, model, scaler, one_hoted_columns_list, file_name = load_data_and_models(data_path, model_path, scaler_path, one_hoted_columns_list_path)

    df, rows_with_na, df_excluded_columns, columns_order, df_aluno_contemplado = preprocess_dataframe(df, one_hoted_columns_list)

    df = postprocess_dataframe(df, model, scaler, rows_with_na, df_excluded_columns, columns_order, file_name)

    validate_df(df, df_aluno_contemplado, file_name)

if __name__ == "__main__":
    main()