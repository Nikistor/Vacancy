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
        model = CustomUser
        fields = ('id', 'name', 'email', 'is_moderator')


class VacancySerializer(serializers.ModelSerializer):
    cities = CitySerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True, many=False)

    class Meta:
        # Модель, которую мы сериализуем
        model = Vacancy
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

