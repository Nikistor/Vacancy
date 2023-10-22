from bmstu_lab.models import City, Vacancy, VacancyCity, Users
from rest_framework import serializers

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = City
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'

class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Vacancy
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'

class VacancyCitySerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = VacancyCity
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Users
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'