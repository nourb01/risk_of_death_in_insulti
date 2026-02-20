from django.shortcuts import render, redirect
from .forms import StrokeForm
from functions import predict_stroke_risk, ask_Giga
import traceback

# Create your views here.
def index(request):
    #первая, не по объему, а по вложенной любви страница
    return render(request, 'main/index.html')
def anketa(request):
    #страница, на которой даем слово пациенту
    if request.method == 'POST':
        form = StrokeForm(request.POST)
        if form.is_valid():
            entry = form.save()
            patient_data = {
                #формализуем и сортируем роскозни клиента, что не вгонять нашу модель в депрессию
                'age': float(entry.age),
                'hypertension': int(entry.hypertension),
                'heart_disease': int(entry.heart_disease),
                'avg_glucose_level': float(entry.avg_glucose_level),
                'bmi': float(entry.bmi),

                'gender_male': int(entry.gender == 'male'),
                'gender_other': 0,
                'ever_married_Yes': int(entry.ever_married == 'Yes'),
                'Residence_type_Urban': int(entry.residence_type == 'Urban'),

                'smoking_status_formerly smoked': int(entry.smoking_status == 'formerly smoked'),
                'smoking_status_never smoked': int(entry.smoking_status == 'never smoked'),
                'smoking_status_smokes': int(entry.smoking_status == 'smokes'),

                'work_type_Private': int(entry.work_type == 'Private'),
                'work_type_Self-employed': int(entry.work_type == 'Self-employed'),
                'work_type_Govt_job': int(entry.work_type == 'Govt_job'),
                'work_type_children': int(entry.work_type == 'children'),
                'work_type_Never_worked': int(entry.work_type == 'Never_worked'),
            }
            request.session['patient_info'] = patient_data
            try:
                result = predict_stroke_risk(patient_data)
                request.session['ai_result'] = result
                return redirect('ansver')
            except Exception as e:
                print("ОШИБКА:")
                traceback.print_exc()
                return render(request, 'main/anketa.html', {'form': form, 'error': str(e)})
    else:
        form = StrokeForm()
    return render(request, 'main/anketa.html', {'form': form})

def ansver(request):
    #даем слово нейросетям
        result = request.session.get('ai_result')
        print(f"Данные в сессии: {result}")
        res_fl = result['Вероятность_инсульта'].replace('%', '').replace(',', '.')
        probability = float(res_fl)
        if probability>50.0:
            patient_info = request.session.get('patient_info')
            sovet = ask_Giga(patient_info, result['Риск_инсульта'], result['Вероятность_инсульта'])
        else:
            sovet = "Ваши показатели в норме. Особых распоряжений от ИИ нет, продолжайте вести здоровый образ жизни!"
        return render(request, 'main/ansver.html', {'result': result, 'sovet': sovet})