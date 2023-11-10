from datetime import datetime

from django.db import models

from django.utils import timezone


class City(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, default="Москва", verbose_name="Название")
    foundation_date = models.IntegerField(default=1147, verbose_name="Дата основания")
    grp = models.BigIntegerField(default=20450000000000, verbose_name="ВВП")
    climate = models.CharField(max_length=255, default="умеренный", verbose_name="Климат")
    square = models.IntegerField(default=2561, verbose_name="Площадь")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    description = models.CharField(max_length=2000, default="Москва — столица и крупнейший город России. Сюда ведут многие пути и человеческие судьбы, с этим городом связано множество роковых и знаменательных событий истории, людских радостей и надежд, несчастий и разочарований, разумеется, легенд, мифов и преданий. Москва — блистательный город, во всех отношениях достойный называться столицей. Здесь великолепные памятники архитектуры и живописные парки, самые лучшие магазины и высокие небоскребы, длинное метро и заполненные вокзалы. Москва никогда не спит, здесь трудятся с утра до поздней ночи, а затем веселятся до утра.", null=True, blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to="cities", default="cities/Москва.jpg", verbose_name="Фото")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


class Vacancy(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершён'),
        (4, 'Отменён'),
        (5, 'Удалён'),
    )

    name = models.CharField(max_length=255, verbose_name="Название")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата создания")
    date_of_formation = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата формирования")
    date_complete = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата завершения")

    cities = models.ManyToManyField(City, verbose_name="Города", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"