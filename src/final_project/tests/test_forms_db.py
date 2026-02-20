from django.test import TestCase, Client
from django.urls import reverse
from main.models import StrokeData

class FormAndDatabaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('anketa')

    def test_correct_data_submission(self):
        """Тест на корректный ввод данных пользователем"""
        payload = {
            'gender': 'male', 'age': 45, 'hypertension': 0,
            'heart_disease': 0, 'ever_married': 'Yes', 'work_type': 'Private',
            'residence_type': 'Urban', 'avg_glucose_level': 95.5,
            'bmi': 24.1, 'smoking_status': 'never smoked'
        }
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(StrokeData.objects.count(), 1)
        self.assertEqual(StrokeData.objects.first().age, 45)

    def test_empty_data_submission(self):
        """Тест на обработку пустых данных"""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StrokeData.objects.count(), 0)

    def test_invalid_data_types(self):
        """Тест на ввод некорректных типов данных"""
        payload = {'age': 'not_a_number', 'gender': 'male'}
        response = self.client.post(self.url, data=payload)
        self.assertFormError(response, 'form', 'age', 'Enter a number.')