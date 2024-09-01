import pandas as pd
from joblib import load
from utils.utils import remove_initial_and_ending_spaces, convert_columns_to_float64, revert_one_hot, filling_missing_columns, reorder_columns
from utils.constants import columns_white_list, columns_to_float64, one_hot_encoding_columns
from datetime import datetime
import warnings



# Fazendo com que as saídas de alerta sejam ignoradas
warnings.filterwarnings('ignore')

# Carrega o arquivo a ser analisado, o modelo que irá analisar e o scaler de normalização
df = pd.read_excel("./data/IFPE_10.xlsx")
model = load('./models/GBM_80c_a87.joblib')
scaler = load('./models/scalers/std_scaler_GBM_80c_a87.pkl')

# Remove espaços em branco nos nomes das colunas
for col in df.columns:
    df = df.rename({col:remove_initial_and_ending_spaces(col)}, axis='columns')

# Verifica se o df tem o resultado da escolha da bolsa (PURAMENTE PARA TESTES!!!)
resultado_flag = False
if "Aluno contemplado com bolsa?" in df.columns:
    resultado_flag = True

# Renomeia erro de português em uma das colunas
if "Condiçõees de moradia familiar" in df:
    df.rename(columns={"Condiçõees de moradia familiar": "Condições de moradia familiar"}, inplace=True)

# Armazenando a ordem do dataframe antes dos próximos preprocessamentos
columns_order = df.columns.tolist()

# Lendo o arquivo txt e criando uma lista com as colunas necessárias para o dataframe ser passado no modelo
with open('./src/utils/model_72_columns.txt', 'r', encoding='ISO-8859-1') as file:
    necessary_columns = file.read().splitlines()

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

# One-hot encoding (provavelmente será removido)
df = pd.get_dummies(df, columns=one_hot_encoding_columns, drop_first=False)

# Preenchendo possíveis colunas faltantes (especialmente as de one-hot encoding que dependem da entrada para existir)
df = filling_missing_columns(df, necessary_columns)

# Ordena os index baseados nas colunas
df.sort_index(axis=1, inplace=True)

# Troca valores 'Sim' para True e 'Não' para False, para ser passado no modelo
df.replace({'Sim': True, 'Não': False}, inplace=True)

# Transforma valores negativos em 0
numeric_df = df.select_dtypes(include=['number'])
numeric_df_clipped = numeric_df.clip(lower=0)
df[numeric_df_clipped.columns] = numeric_df_clipped

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
df = reorder_columns(df, columns_order, resultado_flag) # DEVE SER COLOCADO FALSE ANTES DO LANÇAMENTO!!!!

# dataframe com uma coluna extra de aptidão, para verificar o desempenho do sistema (DEVE SER REMOVIDO ANTES DE LANÇAR)
df_validation = pd.concat([df, df_aluno_contemplado], axis=1) # (DEVE SER REMOVIDO ANTES DE LANÇAR)

# Renomeia de volta os valores que eram 'Sim' e 'Não'
df.replace({True: 'Sim', False: 'Não'}, inplace=True)

# Renomeia de volta os valores que eram 'Sim' e 'Não'
df_validation.replace({True: 'Sim', False: 'Não'}, inplace=True)

# Renomeando a coluna "Data de nascimento" para "Idade"
df = df.rename(columns={'Data de nascimento': 'Idade'})

# Salva a planilha reordenada
df.to_excel('./data/cleaned_datas/cleaned_IFPE_10.xlsx', index=False)

# Salva a planilha reordenada
df_validation.to_excel('./data/cleaned_datas/cleaned_IFPE_10_validation.xlsx', index=False)