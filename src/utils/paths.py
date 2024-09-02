import os

data_path = './data/raw_data/IFPE_10.xlsx'

model_path = './models/GBM_71c_a0.8207941483803552.joblib'

model_name = os.path.basename(model_path)
scaler_path = f'./models/scalers/std_scaler_{model_name.split('.')[0]}.{model_name.split('.')[1]}.pkl'

one_hoted_columns_list_path = './src/utils/model_71_columns.txt'