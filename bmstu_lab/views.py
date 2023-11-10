from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .models import *


@api_view(["GET"])
def search_city(request):
    """
    Возвращает список городов
    """

    # Получим параметры запроса из URL
    name = request.GET.get('name')
    foundation_date = request.GET.get('foundation_date')
    grp = request.GET.get('grp')
    climate = request.GET.get('climate')
    square = request.GET.get('square')
    description = request.GET.get('description')

    # Получение данные после запроса с БД (через ORM)
    city = City.objects.filter(status=1)

    # Применим фильтры на основе параметров запроса, если они предоставлены
    if name:
        city = city.filter(name__icontains=name)
    if foundation_date:
        city = city.filter(foundation_date=foundation_date)
    if grp:
        city = city.filter(grp=grp)
    if climate:
        city = city.filter(climate__icontains=climate)
    if square:
        city = city.filter(square=square)
    if description:
        city = city.filter(description__icontains=description)

    serializer = CitySerializer(city, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_city_by_id(request, city_id):
    """
    Возвращает информацию о конкретном городе
    """
    if not City.objects.filter(pk=city_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Получение данные после запроса с БД (через ORM)
    city = City.objects.get(pk=city_id)

    serializer = CitySerializer(city, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def update_city(request, city_id):
    """
    Обновляет информацию о городе
    """

    if not City.objects.filter(pk=city_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    city = City.objects.get(pk=city_id)
    serializer = CitySerializer(city, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_city(request):
    """
    Добавляет новый город
    """
    City.objects.create()

    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_city(request, city_id):
    """
    Удаляет город
    """
    if not City.objects.filter(pk=city_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    city = City.objects.get(pk=city_id)
    city.status = 2
    city.save()

    cities = City.objects.filter(status=1)
    serializer = CitySerializer(cities, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_city_to_vacancy(request, city_id):
    """
    Добавляет город в вакансию
    """

    if not City.objects.filter(pk=city_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    city = City.objects.get(pk=city_id)

    vacancy = Vacancy.objects.filter(status=1).last()

    if vacancy is None:
        vacancy = Vacancy.objects.create()

    vacancy.cities.add(city)
    vacancy.save()

    serializer = VacancySerializer(vacancy.cities, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_city_image(request, city_id):
    """
    Возвращает фото города
    """
    if not City.objects.filter(pk=city_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    service = City.objects.get(pk=city_id)

    return HttpResponse(service.image, content_type="image/png")


@api_view(["PUT"])
def update_city_image(request, city_id):
    """
    Обновляет фото города
    """
    if not City.objects.filter(pk=city_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    city = City.objects.get(pk=city_id)
    serializer = CitySerializer(city, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


# @api_view(["GET"])
# def get_vacancies(request):
#     """
#     Возвращает список вакансий
#     """
#     vacancies = Vacancy.objects.all()
#
#     request_status = request.GET.get("status")
#     if request_status:
#         vacancies = vacancies.filter(status=request_status)
#
#     serializer = VacancySerializer(vacancies, many=True)
#
#     return Response(serializer.data)

@api_view(["GET"])
def get_vacancies(request):
    """
    Возвращает список вакансий
    """
    vacancies = Vacancy.objects.all()

    # Получим параметры запроса из URL
    status = request.GET.get('status')
    date_created = request.GET.get('date_created')
    date_complete = request.GET.get('date_complete')
    date_form_after = request.GET.get('date_form_after')
    date_form_before = request.GET.get('date_form_before')

    # Применим фильтры на основе параметров запроса, если они предоставлены
    if status:
        vacancies = vacancies.filter(status=status)
    if date_created:
        vacancies = vacancies.filter(date_created=date_created)
    if date_complete:
        vacancies = vacancies.filter(date_complete=date_complete)

    # Дата формирования ПОСЛЕ
    if date_form_after and date_form_before is None:
        vacancies = vacancies.filter(date_of_formation__gte=date_form_after)
    # Дата формирования ДО
    if date_form_after is None and date_form_before:
        vacancies = vacancies.filter(date_of_formation__lte=date_form_before)

    # Дата формирования ПОСЛЕ и ДО
    if date_form_after and date_form_before:
        if date_form_after > date_form_before:
            return Response('Mistake! It is impossible to sort when "BEFORE" exceeds "AFTER"!')
        vacancies = vacancies.filter(date_of_formation__gte=date_form_after, date_of_formation__lte=date_form_before)

    serializer = VacancySerializer(vacancies, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_vacancy_by_id(request, vacancy_id):
    """
    Возвращает информацию о конкретной вакансии
    """
    if not Vacancy.objects.filter(pk=vacancy_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    vacancy = Vacancy.objects.get(pk=vacancy_id)
    serializer = VacancySerializer(vacancy, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_vacancy(request, vacancy_id):
    """
    Обновляет информацию о вакансии
    """
    if not Vacancy.objects.filter(pk=vacancy_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    vacancy = Vacancy.objects.get(pk=vacancy_id)
    serializer = VacancySerializer(vacancy, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    vacancy.status = 1
    vacancy.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, vacancy_id):
    """
    Пользователь обновляет информацию о вакансии
    """
    if not Vacancy.objects.filter(pk=vacancy_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    vacancy = Vacancy.objects.get(pk=vacancy_id)
    vacancy.status = 2
    vacancy.save()

    serializer = VacancySerializer(vacancy, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, vacancy_id):
    """
    Модератор обновляет информацию о вакансии
    """
    if not Vacancy.objects.filter(pk=vacancy_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status in [1, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    vacancy = Vacancy.objects.get(pk=vacancy_id)

    lesson_status = vacancy.status

    if lesson_status in [3, 4, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    vacancy.status = request_status
    vacancy.save()

    serializer = VacancySerializer(vacancy, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_vacancy(request, vacancy_id):
    """
    Удаляет вакансию
    """
    if not Vacancy.objects.filter(pk=vacancy_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    vacancy = Vacancy.objects.get(pk=vacancy_id)
    vacancy.status = 5
    vacancy.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_city_from_vacancy(request, vacancy_id, city_id):
    """
    Удаляет город из вакансии
    """
    if not Vacancy.objects.filter(pk=vacancy_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not City.objects.filter(pk=city_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    vacancy = Vacancy.objects.get(pk=vacancy_id)
    vacancy.cities.remove(City.objects.get(pk=city_id))
    vacancy.save()

    serializer = CitySerializer(vacancy.cities, many=True)

    return Response(serializer.data)
