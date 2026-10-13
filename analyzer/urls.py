from django.urls import path
from . import views  # Импорт модуля views из текущего приложения

urlpatterns = [
    path('', views.home, name='home'),
    path('analyze/', views.analyze_page, name='analyze'),
]