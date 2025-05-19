# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, StudentProfileForm
from .models import UserProfile
from vacancies.models import Vacancy


def home_view(request):
    context = {}
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'student':
        vacancies = Vacancy.objects.all().order_by('-created_at')[:10] # Показываем последние 10
        context['vacancies'] = vacancies
    return render(request, 'home.html', context)


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username') # Если нужно автоматически войти
            # user = authenticate(username=username, password=form.cleaned_data.get('password'))
            # login(request, user)
            return redirect('login')  # Или 'home' если авто-логин
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                # Проверяем, есть ли у пользователя профиль и куда его направить
                try:
                    profile = user.userprofile
                    if profile.role == 'student':
                        return redirect('profile_view')  # Предполагаем, что есть такой URL
                    elif profile.role == 'employer':
                        return redirect('my_vacancies')  # Предполагаем, что есть такой URL
                except UserProfile.DoesNotExist:
                    # На случай, если профиль не создался (маловероятно с сигналом)
                    return redirect('home')  # Или страница для завершения профиля
                return redirect('home')
            else:
                form.add_error(None, "Неверный логин или пароль.")
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    # Убедимся, что это студент/выпускник
    if request.user.userprofile.role != 'student':
        return redirect('home')  # Или показать ошибку доступа

    profile = request.user.userprofile
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # Обновить страницу с сообщением об успехе
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'users/profile_view.html', {'form': form, 'profile': profile})