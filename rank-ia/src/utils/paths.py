import os

input_path = './rank-ia/data/raw_data/input.xlsx'

output_path = './rank-ia/data/cleaned_data/output.xlsx'

model_path = './rank-ia/models/GBM_58c_a0.8197492163009404.joblib'

model_name = os.path.basename(model_path)
scaler_path = f'./rank-ia/models/scalers/std_scaler_{model_name.split('.')[0]}.{model_name.split('.')[1]}.pkl'

one_hoted_columns_list_path = './rank-ia/src/utils/model_57_columns.txt'

model_text_path = './rank-ia/models/spacy_model_LR.joblib'

#spacy_path = './rank-ia/models/spacy_model'