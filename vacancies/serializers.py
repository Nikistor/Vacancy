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
        fields = ['login']


class VacancySerializer(serializers.ModelSerializer):
    cities = CitySerializer(read_only=True, many=True)

    employer = UserSerializer(read_only=True)
    moderator = UserSerializer(read_only=True)

    class Meta:
        # Модель, которую мы сериализуем
        model = Vacancy
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'