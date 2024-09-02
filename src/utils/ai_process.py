def ai_process(df, model, scaler):

    # Normaliza os dados
    X = scaler.transform(df)

    # Modelo gera um score do quanto o aluno precisa da bolsa
    y_pred_proba = model.predict_proba(X)

    return df, y_pred_proba