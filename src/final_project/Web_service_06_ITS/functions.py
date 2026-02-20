import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from gigachat import GigaChat

def train_or_retrain_model(df):
    X_data = df.drop('stroke', axis=1)
    y_data = df['stroke']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_data)

    model = LogisticRegression(class_weight='balanced', random_state=42)
    model.fit(X_scaled, y_data)

    return model, scaler, list(X_data.columns)


def save_model(m, s, c):
    joblib.dump(m, 'model.pkl')
    joblib.dump(s, 'scaler.pkl')
    joblib.dump(c, 'columns.pkl')


def load_model():
    m = joblib.load('model.pkl')
    s = joblib.load('scaler.pkl')
    c = joblib.load('columns.pkl')
    return m, s, c


def predict_stroke_risk(patient_dict):
    #связь с моей моделью, чтоб как нибудь рассчитать риск
    m, s, c = load_model()
    df_p = pd.DataFrame(0.0, index=[0], columns=c)

    for key, value in patient_dict.items():
        if key in df_p.columns:
            df_p.loc[0, key] = value

    scaled_data = s.transform(df_p)
    probability = m.predict_proba(scaled_data)[0][1]

    if probability < 0.1:
        cat = "Крайне низкий"
    elif probability < 0.25:
        cat = "Низкий"
    elif probability < 0.5:
        cat = "Значительный"
    elif probability < 0.75:
        cat = "Высокий"
    else:
        cat = "Крайне высокий"

    return {
        "Вероятность_инсульта": f"{probability:.1%}",
        "Риск_инсульта": cat
    }

def ask_Giga(patient_data, risk_label, probability):
    #связь с гигачатом
    gender = "Мужчина" if patient_data.get('gender_male') == 1 else "Женщина"

    prompt = f"""
        Ты — профессиональный врач-консультант кардиолог с огромным опытом. Перед тобой ответы пациента прошедшего анкетирование, а так же результаты оценки риска и вероятности инсульта:
        - Пол: {gender}
        - Возраст: {patient_data['age']} лет
        - Артериальная гипертензия: {'Есть' if patient_data['hypertension'] else 'Нет'}
        - Болезни сердца: {'Есть' if patient_data['heart_disease'] else 'Нет'}
        - Уровень глюкозы: {patient_data['avg_glucose_level']}
        - ИМТ (BMI): {patient_data['bmi']}

        Результат анализа:
        - Риск инсульта: {risk_label}
        - Вероятность: {probability}

        Твоя задача представить список из 3-4 конкретных совета для этого пациента. Отвечай кратко, профессионально и поддерживающе. Твой ответ должен содержать ТОЛЬКО список из советов, не добавляй ничего лишнего и не пиши приветственный текст. Ответ представь в виде списка 1), 2), 3)...... и тд
        """
    giga = GigaChat(
        credentials="MDE5YmJiYWMtZmJhYy03NjM3LTk1MGUtODFjMDRmOTg4YWNmOjkxMWUwZDcxLTEyMDQtNDdhZC1hOTljLWU3YWIwNDhjNmZhYQ==",
        verify_ssl_certs=False)
    response = giga.chat(prompt)
    return response.choices[0].message.content
