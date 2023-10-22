from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from bmstu_lab.serializers import CitySerializer, VacancySerializer, VacancyCitySerializer, UsersSerializer
from bmstu_lab.models import City, Vacancy, VacancyCity, Users
from rest_framework.views import APIView
from rest_framework.decorators import api_view

# Город
class CityList(APIView):
    model_class = City
    serializer_class = CitySerializer

    def get(self, request, format=None):
        """
        Возвращает список городов
        """
        city = self.model_class.objects.all()
        serializer = self.serializer_class(city, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Добавляет новую запись
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            city = serializer.save()  # Сохраняем город
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CityDetail(APIView):
    model_class = City
    serializer_class = CitySerializer

    def get(self, request, pk, format=None):
        """
        Возвращает информацию о городе
        """
        city = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(city)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Обновляет информацию о городе (для модератора)
        """
        city = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(city, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Удаляет информацию о городе
        """
        city = get_object_or_404(self.model_class, pk=pk)
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['Put'])
def put_city_detail(request, pk, format=None):
    """
    Обновляет информацию о городе (для пользователя)
    """
    city = get_object_or_404(City, pk=pk)
    serializer = CitySerializer(city, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Добавляет новую запись в заявку
@api_view(['Post'])
def post_city_in_vacancy(request, city_pk, vacancy_pk, format=None):
    try:
        city = City.objects.get(pk=city_pk)
    except City.DoesNotExist:
        return Response(f"ERROR! Object City does not exist with ID {city_pk}",
                        status=status.HTTP_404_NOT_FOUND)

    try:
        vacancy = Vacancy.objects.get(pk=vacancy_pk)
    except Vacancy.DoesNotExist:
        return Response(f"ERROR! Object Vacancy does not exist with ID {vacancy_pk}",
                        status=status.HTTP_404_NOT_FOUND)

    VacancyCity.objects.create(
        id_city=city,
        id_vacancy=vacancy,
    )
    return Response('Successfully created', status=status.HTTP_201_CREATED)

# Вакансия
class VacancyList(APIView):
    model_class = Vacancy
    serializer_class = VacancySerializer

    def get(self, request, format=None):
        """
        Возвращает список вакансии
        """
        vacancy = self.model_class.objects.all()
        serializer = self.serializer_class(vacancy, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Добавляет новую запись
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VacancyDetail(APIView):
    model_class = Vacancy
    serializer_class = VacancySerializer

    def get(self, request, pk, format=None):
        """
        Возвращает информацию о вакансии
        """
        vacancy = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(vacancy)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Обновляет информацию о вакансии (для модератора)
        """
        vacancy = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(vacancy, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Удаляет информацию о вакансии
        """
        vacancy = get_object_or_404(self.model_class, pk=pk)
        vacancy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['Put'])
def put_vacancy_detail(request, pk, format=None):
    """
    Обновляет информацию о вакансии (для пользователя)
    """
    vacancy = get_object_or_404(Vacancy, pk=pk)
    serializer = VacancySerializer(vacancy, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Put'])
def put_vacancy_BY_EMPLOYER(request, pk, format=None):
    """
    Обновляет информацию о вакансии (для пользователя)
    """
    vacancy = get_object_or_404(Vacancy, pk=pk)
    serializer = VacancySerializer(vacancy, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Put'])
def put_vacancy_BY_MODERATOR(request, pk, format=None):
    """
    Обновляет информацию о вакансии (для пользователя)
    """
    vacancy = get_object_or_404(Vacancy, pk=pk)
    serializer = VacancySerializer(vacancy, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Вакансии города
class VacancyCityList(APIView):
    model_class = VacancyCity
    serializer_class = VacancyCitySerializer

    def get(self, request, format=None):
        """
        Возвращает список вакансии города
        """
        vacancycity = self.model_class.objects.all()
        serializer = self.serializer_class(vacancycity, many=True)
        return Response(serializer.data)

class VacancyCityDetail(APIView):
    model_class = VacancyCity
    serializer_class = VacancyCitySerializer

    def put(self, request, pk, format=None):
        """
        Обновляет информацию о вакансии города (для модератора)
        """
        vacancycity = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(vacancycity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Удаляет информацию о вакансии города
        """
        vacancycity = get_object_or_404(self.model_class, pk=pk)
        vacancycity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

