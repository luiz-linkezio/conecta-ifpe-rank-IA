import os

input_path = '../data/raw_data/input.xlsx'

output_path = '../../api/uploads/processed_output.xlsx'

model_path = '../models/GBM_58c_a0.8197492163009404.joblib'

model_name = os.path.basename(model_path)
scaler_path = f'../models/scalers/std_scaler_{model_name.split('.')[0]}.{model_name.split('.')[1]}.pkl'

one_hoted_columns_list_path = '../src/utils/model_57_columns.txt'

model_text_path = '../models/spacy_model_LR.joblib'

#spacy_path = '../models/spacy_model'