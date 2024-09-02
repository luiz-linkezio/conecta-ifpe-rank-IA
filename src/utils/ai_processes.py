def ai_process_GBM(df, model, scaler):

    # Normaliza os dados
    X = scaler.transform(df)

    # Modelo gera um score do quanto o aluno precisa da bolsa
    y_pred_proba = model.predict_proba(X)
    y_pred_class = model.predict(X)

    return df, y_pred_proba, y_pred_class