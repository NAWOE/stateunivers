# users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Студент/Выпускник'),
        ('employer', 'Работодатель'),
    )
    GENDER_CHOICES = (
        ('male', 'Мужской'),
        ('female', 'Женский'),
    )
    EMPLOYMENT_TYPE_CHOICES = (
        ('full', 'Полная занятость'),
        ('part_time', 'Частичная занятость'),
    )
    SCHEDULE_CHOICES = (
        ('5/2', '5/2'),
        ('2/2', '2/2'),
        ('6/1', '6/1'),
        ('3/3', '3/3'),
        ('flexible', 'Гибкий график'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Пол")
    date_of_birth = models.DateField(verbose_name="Дата Рождения")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name="Роль")

    # Поля для Студента/Выпускника
    skills = models.TextField(blank=True, null=True, verbose_name="Навыки")
    institute = models.CharField(max_length=255, blank=True, null=True, verbose_name="Институт")
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, blank=True, null=True, verbose_name="Тип занятости")
    desired_schedule = models.CharField(max_length=10, choices=SCHEDULE_CHOICES, blank=True, null=True, verbose_name="Желаемый график")

    # Поля для Работодателя (если нужны, например, название компании)
    company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название компании (для работодателя)")

    def __str__(self):
        return self.user.username

# Сигнал для автоматического создания/обновления UserProfile при создании/обновлении User
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist: # На случай если User создан, но профиля нет (например, через createsuperuser)
         UserProfile.objects.create(user=instance)