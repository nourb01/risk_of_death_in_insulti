from django.test import TestCase, Client
from django.urls import reverse
from main.models import StrokeData
from functions import predict_stroke_risk, ask_Giga


class StrokeAppComprehensiveTest(TestCase):
    def setUp(self):
        """Настройка окружения перед каждым тестом"""
        self.client = Client()
        self.anketa_url = reverse('anketa')
        self.sample_ml_data = {
            'age': 65.0, 'hypertension': 1, 'heart_disease': 0,
            'avg_glucose_level': 180.5, 'bmi': 32.2,
            'gender_male': 1, 'gender_other': 0, 'ever_married_Yes': 1,
            'Residence_type_Urban': 1, 'smoking_status_smokes': 1,
            'smoking_status_never smoked': 0, 'smoking_status_formerly smoked': 0,
            'work_type_Private': 1, 'work_type_Self-employed': 0,
            'work_type_Govt_job': 0, 'work_type_children': 0, 'work_type_Never_worked': 0
        }

    # 1. Тестирование корректного ввода и сохранения в базу
    def test_successful_form_submission(self):
        payload = {
            'gender': 'male', 'age': 45, 'hypertension': 0,
            'heart_disease': 0, 'ever_married': 'Yes', 'work_type': 'Private',
            'residence_type': 'Urban', 'avg_glucose_level': 95.5,
            'bmi': 24.1, 'smoking_status': 'never smoked'
        }
        response = self.client.post(self.anketa_url, data=payload)
        self.assertEqual(StrokeData.objects.count(), 1)
        self.assertEqual(response.status_code, 302)

    # 2. Обработка некорректных или пустых данных
    def test_invalid_form_submission(self):
        response = self.client.post(self.anketa_url, data={})
        self.assertEqual(StrokeData.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

    # 3. Генерация прогнозов ML-моделью
    def test_ml_prediction_logic(self):
        result = predict_stroke_risk(self.sample_ml_data)
        self.assertIn('Вероятность_инсульта', result)
        self.assertIn('Риск_инсульта', result)
        self.assertTrue('%' in result['Вероятность_инсульта'])

    # 4. Генерация рекомендаций
    def test_ai_recommendation_logic(self):
        sovet = ask_Giga(self.sample_ml_data, "Высокий", "88.5%")
        self.assertIsInstance(sovet, str)
        self.assertTrue(len(sovet) > 0)