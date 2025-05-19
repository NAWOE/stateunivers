# users/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label="Логин (Email)", widget=forms.EmailInput)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    # Поля для UserProfile
    full_name = forms.CharField(label="ФИО")
    gender = forms.ChoiceField(label="Пол", choices=UserProfile.GENDER_CHOICES)
    date_of_birth = forms.DateField(label="Дата Рождения", widget=forms.DateInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(label="Номер телефона")
    role = forms.ChoiceField(label="Роль", choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User  # Базовая модель для username, email, password
        fields = ('username', 'full_name', 'gender', 'date_of_birth', 'phone_number', 'role')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']

    def clean_username(self):  # Используем email как username
        username = self.cleaned_data['username']
        if User.objects.filter(email=username).exists():  # Проверяем email, т.к. он будет username
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return username

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],  # email будет логином
            email=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        # UserProfile создается автоматически через сигнал, но мы обновим поля
        user.userprofile.full_name = self.cleaned_data['full_name']
        user.userprofile.gender = self.cleaned_data['gender']
        user.userprofile.date_of_birth = self.cleaned_data['date_of_birth']
        user.userprofile.phone_number = self.cleaned_data['phone_number']
        user.userprofile.role = self.cleaned_data['role']

        if commit:
            user.save()  # Сохранит User, что вызовет сигнал и сохранит UserProfile
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Логин (Email)")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")


# Форма для редактирования профиля студента/выпускника
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['skills', 'institute', 'employment_type', 'desired_schedule']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
        }