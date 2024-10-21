def ai_process_GBM(df, model, scaler):

    # Normaliza os dados
    X = scaler.transform(df)

    # Modelo gera um score do quanto o aluno precisa da bolsa
    y_pred_proba = model.predict_proba(X)
    y_pred_class = model.predict(X)

    return df, y_pred_proba, y_pred_class

def ai_process_spacy(df, nlp, model):

    list_df_text_column = list(map(str, df))

    def get_embeddings(text):
        doc = nlp(text)
        return doc.vector

    def predict_score(text):
        embedding = get_embeddings(text).reshape(1, -1)  # Necessário para compatibilidade com o modelo
        return model.predict_proba(embedding)[0][1]  # Probabilidade da classe positiva (necessidade de bolsa)

    pred_df_text_column = [predict_score(text) for text in list_df_text_column] 

    return pred_df_text_column