from django.db import models

# Create your models here.
# Пользователь
class Users(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=120)
    admin = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'users'

# Город
class City(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    name = models.CharField(max_length=100)
    foundation_date = models.IntegerField(null=True, blank=True)
    grp = models.FloatField(null=True, blank=True)
    climate = models.CharField(max_length=255, null=True, blank=True)
    square = models.IntegerField(null=True, blank=True)
    status = models.BooleanField()
    description = models.CharField(max_length=2000, null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'city'

# Вакансия
class Vacancy(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    name_vacancy = models.CharField(max_length=255)
    date_create = models.DateField()
    date_form = models.DateField(blank=True, null=True)
    date_close = models.DateField(blank=True, null=True)
    status_vacancy = models.CharField(max_length=50)
    id_employer = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='id_employer',  # Имя поля в базе данных
    )
    id_moderator = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='id_moderator',  # Имя поля в базе данных
        related_name='id_employer_moderator',  # Пользовательское имя
    )
    class Meta:
        managed = False
        db_table = 'vacancy'

# ВакансииГорода
class VacancyCity(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    # Добавляем внешний ключ к другой модели
    id_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='id_city',  # Имя поля в базе данных
    )
    id_vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='id_vacancy',  # Имя поля в базе данных
    )
    class Meta:
        managed = False
        db_table = 'vacancycity'