# vacancies/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.vacancy_list_view, name='vacancy_list'),
    path('my/', views.my_vacancies_view, name='my_vacancies'),
    path('create/', views.vacancy_create_view, name='vacancy_create'),
    path('<int:pk>/', views.vacancy_detail_view, name='vacancy_detail'),
    path('<int:pk>/update/', views.vacancy_update_view, name='vacancy_update'),
    path('<int:pk>/delete/', views.vacancy_delete_view, name='vacancy_delete'),
]