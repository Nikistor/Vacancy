from rest_framework import serializers
from .models import *


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = City
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['login']  # Укажите необходимые поля пользователя

class VacancySerializer(serializers.ModelSerializer):
    cities = CitySerializer(read_only=True, many=True)
    users = UserSerializer(read_only=True)  # Добавьте поле пользователя в сериализатор

    class Meta:
        # Модель, которую мы сериализуем
        model = Vacancy
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'