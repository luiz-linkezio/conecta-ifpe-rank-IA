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
    for column in columns_to_float64:
        df[column] = pd.to_numeric(df[column], errors='coerce').astype('float64')
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