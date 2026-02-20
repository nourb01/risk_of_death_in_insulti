from django import forms
from .models import StrokeData


class StrokeForm(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=[('male', 'Мужской'), ('female', 'Женский')],
        widget=forms.RadioSelect,
        label="Пол"
    )
    class Meta:
        model = StrokeData
        fields = [
            'gender', 'age', 'hypertension', 'heart_disease',
            'ever_married', 'work_type', 'residence_type',
            'avg_glucose_level', 'bmi', 'smoking_status'
        ]

        widgets = {

            'ever_married': forms.RadioSelect(),
            'work_type': forms.RadioSelect(),
            'residence_type': forms.RadioSelect(),
            'smoking_status': forms.RadioSelect(),
            'hypertension': forms.RadioSelect(choices=[(1, 'Да'), (0, 'Нет')]),
            'heart_disease': forms.RadioSelect(choices=[(1, 'Да'), (0, 'Нет')]),

            'age': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Возраст'}),
            'avg_glucose_level': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Глюкоза'}),
            'bmi': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'ИМТ'}),
        }