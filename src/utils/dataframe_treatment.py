import re
import pandas as pd

def remove_initial_and_ending_spaces(name):
    regex = r'^(?:\s+)?(?P<gp>.+?)(?:\s+)?$'
    mo = re.search(regex, name)
    if mo is not None:
      return mo['gp']
    else:
      print(f'Deu erro em: {name}')
      return name
  
def convert_columns_to_float64(df, columns_to_float64):
    try:
        for column in columns_to_float64:
            df[column] = pd.to_numeric(df[column], errors='coerce').astype('float64')
    except:
        pass

    return df

def find_missing_columns(dfs):
    # Cria conjuntos de colunas para cada DataFrame
    column_sets = [set(df.columns) for df in dfs]
    
    # Encontra a interseção das colunas
    common_cols = set.intersection(*column_sets)
    
    # Encontra a união de todas as colunas
    all_cols = set.union(*column_sets)
    
    # Identifica colunas que não estão presentes em todos os DataFrames
    missing_cols = all_cols - common_cols
    
    print("Colunas que não estão presentes em todos os DataFrames:")
    print(missing_cols)
    #print(common_cols)
    print("Número de colunas que não estão presentes em todos os DataFrames:", len(missing_cols))
    #print("Número de colunas que estão presentes em todos os DataFrames:", len(common_cols))

def revert_one_hot(df_encoded, one_hot_columns):
    """
    Revert One-Hot Encoding for the specified columns in the DataFrame.
    
    Parameters:
    - df_encoded (pd.DataFrame): DataFrame with One-Hot Encoded columns.
    - one_hot_columns (list): List of base columns that were one-hot encoded.

    Returns:
    - pd.DataFrame: DataFrame with One-Hot Encoding reverted.
    """
    df_reverted = df_encoded.copy()
    
    for column in one_hot_columns:
        # Get the columns related to this one-hot encoded feature
        one_hot_cols = [col for col in df_encoded.columns if col.startswith(column + '_')]
        
        if one_hot_cols:
            # Revert the one-hot encoding
            df_reverted[column] = df_encoded[one_hot_cols].idxmax(axis=1).str.replace(column + '_', '')
            
            # Drop the one-hot encoded columns
            df_reverted.drop(columns=one_hot_cols, inplace=True)
    
    return df_reverted

def filling_missing_columns(df, necessary_columns):
    missing_columns = [col for col in necessary_columns if col not in df.columns]

    # Adiciona as colunas faltantes com valor False
    for col in missing_columns:
        df[col] = False

    return df

def reorder_columns(df, sorted_columns, test_flag=False):
    common_columns = [col for col in sorted_columns if col in df.columns]
    extra_columns = [col for col in df.columns if col not in common_columns]

    new_column_order = common_columns + extra_columns

    df = df[new_column_order]

    if test_flag == True:
        df = df.drop(columns=["Aluno contemplado com bolsa?"])

    return df

def convert_negative_numbers_to_zero(df):
    numeric_df = df.select_dtypes(include=['number'])
    numeric_df_clipped = numeric_df.clip(lower=0)
    df[numeric_df_clipped.columns] = numeric_df_clipped

    return df

def get_invalid_rows(df):

    numeric_columns = df.select_dtypes(include=['number']).columns
    non_numeric_columns = df.select_dtypes(exclude=['number']).columns

    # 1. Linhas com valores NaN em qualquer coluna
    invalid_rows = df[df.isna().any(axis=1)]

    # 2. Linhas com valores numéricos em colunas não numéricas
    for col in non_numeric_columns:
        numeric_in_non_numeric = df[pd.to_numeric(df[col], errors='coerce').notna()]
        invalid_rows = pd.concat([invalid_rows, numeric_in_non_numeric])

    # 3. Linhas com valores não numéricos em colunas numéricas
    for col in numeric_columns:
        non_numeric_in_numeric = df[~pd.to_numeric(df[col], errors='coerce').notna()]
        invalid_rows = pd.concat([invalid_rows, non_numeric_in_numeric])

    # Remove duplicatas
    invalid_rows = invalid_rows.drop_duplicates()

    return invalid_rows

def drop_common_rows_from_left_df(df_1, df_2):
    # Faz a junção dos dois dataframes, marcando a origem das linhas com o parâmetro 'indicator'
    condition = ~df_1.isin(df_2.to_dict(orient='list')).all(axis=1)
    
    # Filtra as linhas de A que não estão em B
    df_1_filtered = df_1[condition]

    return df_1_filtered