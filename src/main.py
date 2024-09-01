import pandas as pd

from joblib import load

from utils.utils import remove_initial_and_ending_spaces, convert_columns_to_float64, revert_one_hot, find_missing_columns
from utils.constants import columns_white_list, columns_to_float64, one_hot_encoding_columns

from datetime import datetime

import os



df = pd.read_excel("./data/IFPE_10.xlsx")

for col in df.columns:
    df = df.rename({col:remove_initial_and_ending_spaces(col)}, axis='columns')

df = df.drop_duplicates()

df['Data de nascimento'] = (datetime.now() - df['Data de nascimento']).dt.days // 365
df['Data de nascimento'] = df['Data de nascimento'].astype(float)

if "Condiçõees de moradia familiar" in df:
    df.rename(columns={"Condiçõees de moradia familiar": "Condições de moradia familiar"}, inplace=True)

df_excluded_columns = df[df.columns.difference(columns_white_list)]
df = df[columns_white_list]

df = df.drop(columns=["Relato de vida"])
df = df.drop(columns=["Aluno contemplado com bolsa?"])

df = convert_columns_to_float64(df, columns_to_float64)

rows_with_na = df[df.isna().any(axis=1)]
df = df.dropna(axis=0)

df = pd.get_dummies(df, columns=one_hot_encoding_columns, drop_first=False)

df.replace({'Sim': True, 'Não': False}, inplace=True)

numeric_df = df.select_dtypes(include=['number'])
numeric_df_clipped = numeric_df.clip(lower=0)
df[numeric_df_clipped.columns] = numeric_df_clipped

model = load('./models/GBM_80c_a83.joblib')
scaler = load('./models/scalers/std_scaler_GBM_80c_a83.pkl')

df.sort_index(axis=1, inplace=True)
df.reset_index(drop=True, inplace=True)
df_excluded_columns.sort_index(axis=1, inplace=True)
df_excluded_columns.reset_index(drop=True, inplace=True)

X = scaler.transform(df)

y_pred_proba = model.predict_proba(X)

df['Nível de necessidade'] = y_pred_proba[:, 1]

df = df.sort_values(by='Nível de necessidade', ascending=False)
df.reset_index(drop=True, inplace=True)

rows_with_na.sort_index(axis=1, inplace=True)
rows_with_na.reset_index(drop=True, inplace=True)

df = revert_one_hot(df, one_hot_encoding_columns)

df = pd.concat([df, rows_with_na])
#df = pd.concat([df, df_excluded_columns], axis=1)

df.replace({True: 'Sim', False: 'Não'}, inplace=True)

print(len(df))
print(len(df_excluded_columns))

df.to_excel('./data/cleaned_datas/cleaned_IFPE_10.xlsx', index=False)