from django.db import models


class StrokeData(models.Model):
    GENDER_CHOICES = [('male', 'Мужской'), ('female', 'Женский')]
    MARRIED_CHOICES = [('Yes', 'Да'), ('No', 'Нет')]
    WORK_CHOICES = [
        ('Private', 'Частный сектор'),
        ('Self-employed', 'Самозанятый'),
        ('Govt_job', 'Госслужащий'),
        ('children', 'Ребенок'),
        ('Never_worked', 'Никогда не работал')
    ]
    RESIDENCE_CHOICES = [('Urban', 'Город'), ('Rural', 'Село')]
    SMOKING_CHOICES = [
        ('formerly smoked', 'Ранее курил(а)'),
        ('never smoked', 'Никогда не курил(а)'),
        ('smokes', 'Курю'),
        ('Unknown', 'Неизвестно')
    ]

    gender = models.CharField(max_length=10, default='Male',choices=GENDER_CHOICES, verbose_name="Пол")
    age = models.FloatField(verbose_name="Возраст")
    hypertension = models.BooleanField(default=False, verbose_name="Гипертония")
    heart_disease = models.BooleanField(default=False, verbose_name="Болезни сердца")
    ever_married = models.CharField(max_length=5, default='Нет', choices=MARRIED_CHOICES, verbose_name="Состоите ли в браке")
    work_type = models.CharField(max_length=20, default='Никогда не работал', choices=WORK_CHOICES, verbose_name="Тип работы")
    residence_type = models.CharField(max_length=10, default='Город', choices=RESIDENCE_CHOICES, verbose_name="Место жительства")
    avg_glucose_level = models.FloatField(verbose_name="Средний уровень глюкозы")
    bmi = models.FloatField(null=True, blank=True, verbose_name="Индекс массы тела (ИМТ)")
    smoking_status = models.CharField(max_length=20, default='Курю', choices=SMOKING_CHOICES, verbose_name="Статус курения")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Анкета {self.id} - {self.age} лет"