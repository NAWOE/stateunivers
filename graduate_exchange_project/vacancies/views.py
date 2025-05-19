# vacancies/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Vacancy
from .forms import VacancyForm
from users.models import UserProfile  # Для проверки роли


# Декоратор для проверки роли работодателя
def employer_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.userprofile.role == 'employer':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Доступ запрещен: только для работодателей.")

    return wrap


@login_required
def vacancy_list_view(request):
    """Просмотр списка всех вакансий (для студентов/выпускников)"""
    vacancies = Vacancy.objects.all().order_by('-created_at')
    return render(request, 'vacancies/vacancy_list.html', {'vacancies': vacancies})


@login_required
def vacancy_detail_view(request, pk):
    """Просмотр деталей одной вакансии"""
    vacancy = get_object_or_404(Vacancy, pk=pk)
    return render(request, 'vacancies/vacancy_detail.html', {'vacancy': vacancy})


@login_required
@employer_required
def my_vacancies_view(request):
    """Просмотр вакансий, созданных текущим работодателем"""
    vacancies = Vacancy.objects.filter(employer_profile=request.user.userprofile).order_by('-created_at')
    return render(request, 'vacancies/my_vacancies.html', {'vacancies': vacancies})


@login_required
@employer_required
def vacancy_create_view(request):
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.employer_profile = request.user.userprofile  # Связываем с профилем текущего юзера
            vacancy.save()
            return redirect('my_vacancies')  # или 'vacancy_detail' новой вакансии
    else:
        form = VacancyForm()
    return render(request, 'vacancies/vacancy_form.html', {'form': form, 'form_title': 'Создать новую вакансию'})


@login_required
@employer_required
def vacancy_update_view(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    if vacancy.employer_profile != request.user.userprofile:
        return HttpResponseForbidden("Вы не можете редактировать эту вакансию.")

    if request.method == 'POST':
        form = VacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            return redirect('my_vacancies')  # или 'vacancy_detail', pk=vacancy.pk
    else:
        form = VacancyForm(instance=vacancy)
    return render(request, 'vacancies/vacancy_form.html', {'form': form, 'form_title': 'Редактировать вакансию'})


@login_required
@employer_required
def vacancy_delete_view(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    if vacancy.employer_profile != request.user.userprofile:
        return HttpResponseForbidden("Вы не можете удалить эту вакансию.")

    if request.method == 'POST':  # Подтверждение удаления
        vacancy.delete()
        return redirect('my_vacancies')
    # Показываем страницу подтверждения
    return render(request, 'vacancies/vacancy_confirm_delete.html', {'vacancy': vacancy})