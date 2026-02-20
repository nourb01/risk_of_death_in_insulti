from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('anketa/', views.anketa, name='anketa'),
    path('ansver/', views.ansver, name='ansver'),
]