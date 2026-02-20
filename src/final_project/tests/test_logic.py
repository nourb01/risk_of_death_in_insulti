from django.test import TestCase
from functions import predict_stroke_risk, ask_Giga

class MLAndAiLogicTest(TestCase):
    def setUp(self):
        self.ml_input = {
            'age': 70.0, 'hypertension': 1, 'heart_disease': 1,
            'avg_glucose_level': 200.0, 'bmi': 35.0,
            'gender_male': 1, 'gender_other': 0, 'ever_married_Yes': 1,
            'Residence_type_Urban': 1, 'smoking_status_smokes': 1,
            'smoking_status_never smoked': 0, 'smoking_status_formerly smoked': 0,
            'work_type_Private': 1, 'work_type_Self-employed': 0,
            'work_type_Govt_job': 0, 'work_type_children': 0, 'work_type_Never_worked': 0
        }

    def test_ml_prediction_format(self):
        """Тест генерации прогноза"""
        result = predict_stroke_risk(self.ml_input)
        self.assertIn('Вероятность_инсульта', result)
        self.assertIn('Риск_инсульта', result)
        self.assertTrue(result['Вероятность_инсульта'].endswith('%'))

    def test_gigachat_call_format(self):
        """Тест генерации рекомендаций"""
        sovet = ask_Giga(self.ml_input, "Высокий", "85%")
        self.assertIsInstance(sovet, str)
        self.assertGreater(len(sovet), 0)