# vacancies/models.py
from django.db import models
from django.conf import settings  # Для связи с User
# UserProfile нужен для отображения имени компании, если оно есть
from users.models import UserProfile


class Vacancy(models.Model):
    employer_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='vacancies',
                                         limit_choices_to={'role': 'employer'})
    title = models.CharField(max_length=255, verbose_name="Название вакансии")
    description = models.TextField(verbose_name="Описание вакансии")
    requirements = models.TextField(verbose_name="Требования к кандидату")
    salary_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                      verbose_name="Зарплата от")
    salary_to = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Зарплата до")
    company_name_override = models.CharField(max_length=255, blank=True, null=True,
                                             verbose_name="Название компании (если отличается от профиля)")
    # Можно добавить город, тип занятости для вакансии и т.д.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def display_company_name(self):
        if self.company_name_override:
            return self.company_name_override
        if self.employer_profile and self.employer_profile.company_name:
            return self.employer_profile.company_name
        return self.employer_profile.user.username  # Фоллбэк на username, если нет названия компании