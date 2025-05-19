# vacancies/forms.py
from django import forms
from .models import Vacancy

class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'description', 'requirements', 'salary_from', 'salary_to', 'company_name_override']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'title': 'Название вакансии',
            'description': 'Подробное описание',
            'requirements': 'Требования к кандидату',
            'salary_from': 'Зарплата от (руб.)',
            'salary_to': 'Зарплата до (руб.)',
            'company_name_override': 'Название компании (если отличается от профиля или не указано там)'
        }