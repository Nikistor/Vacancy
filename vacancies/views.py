from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import create_access_token
from .permissions import *
from .serializers import *
from .models import *
from dateutil import parser as date_parser

access_token_lifetime = settings.JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()


@api_view(["GET"])
def search_city(request):
    """
    Возвращает список городов
    """

    def get_draft_vacancy_id():
        vacancy = Vacancy.objects.filter(status=1).first()
        # token = get_access_token(request)
        # payload = get_jwt_payload(token)
        # user_id = payload["user_id"]
        # vacancy = Vacancy.objects.filter(employer_id=user_id).filter(status=1).first()

        if vacancy is None:
            return None

        return vacancy.pk

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

    resp = {
        "draft_vacancy": get_draft_vacancy_id(),
        "cities": serializer.data
    }

    return Response(resp)


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
@permission_classes([IsModerator])
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
@permission_classes([IsModerator])
def create_city(request):
    """
    Добавляет новый город
    """
    City.objects.create()

    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsModerator])
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
@permission_classes([IsAuthenticated])
def add_city_to_vacancy(request, city_id):
    """
    Добавляет город в вакансию
    """
    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    if not City.objects.filter(pk=city_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    city = City.objects.get(pk=city_id)

    vacancy = Vacancy.objects.filter(status=1).last()

    if vacancy is None:
        vacancy = Vacancy.objects.create(date_created=datetime.now(timezone.utc), date_of_formation=None, date_complete=None)

    vacancy.employer = CustomUser.objects.get(pk=user_id)
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
@permission_classes([IsModerator])
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_vacancies(request):
    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user = CustomUser.objects.get(pk=payload["user_id"])

    status_id = int(request.GET.get("status", -1))
    user_id = int(request.GET.get("user", -1))
    date_form_after = request.GET.get("date_form_after")
    date_form_before = request.GET.get("date_form_before")

    vacancies = Vacancy.objects.exclude(status__in=[1, 5]) if user.is_moderator else Vacancy.objects.filter(employer_id=user.pk)

    if status_id != -1:
        vacancies = vacancies.filter(status=status_id)

    if user_id != -1:
        vacancies = vacancies.filter(employer_id=user_id)

    if date_form_after:
        vacancies = vacancies.filter(date_of_formation__gte=datetime.strptime(date_form_after, "%Y-%m-%d").date())

    if date_form_before:
        vacancies = vacancies.filter(date_of_formation__lte=datetime.strptime(date_form_before, "%Y-%m-%d").date())

    serializer = VacancySerializer(vacancies, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def update_vacancy(request, vacancy_id):
    """
    Обновляет информацию о вакансии
    """
    if not Vacancy.objects.filter(pk=vacancy_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    vacancy = Vacancy.objects.get(pk=vacancy_id)
    # request.data['date_of_formation'] = None
    # request.data['date_complete'] = None
    serializer = VacancySerializer(vacancy, data=request.data, many=False, partial=True)

    # if 'status' in request.data and request.data['status'] == 1:
    #     request.data['moderator'] = None

    if serializer.is_valid():
        # serializer.validated_data['moderator'] = None
        serializer.save()

    # vacancy.status = 1
    # vacancy.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsRemoteService])
def update_vacancy_bankrupt(request, vacancy_id):
    if not Vacancy.objects.filter(pk=vacancy_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    vacancy = Vacancy.objects.get(pk=vacancy_id)
    serializer = VacancySerializer(vacancy, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, vacancy_id):
    """
    Пользователь обновляет информацию о вакансии
    """
    if not Vacancy.objects.filter(pk=vacancy_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    vacancy = Vacancy.objects.get(pk=vacancy_id)

    if vacancy.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        vacancy.status = 2
        vacancy.save()
        if vacancy.status == 2:
            vacancy.date_of_formation = datetime.now()
            vacancy.save()

    serializer = VacancySerializer(vacancy, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, vacancy_id):
    """
    Модератор обновляет информацию о вакансии
    """
    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    if not Vacancy.objects.filter(pk=vacancy_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    vacancy = Vacancy.objects.get(pk=vacancy_id)

    if vacancy.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if request_status == 3:
        vacancy.date_complete = None
    else:
        vacancy.date_complete = datetime.now()

    vacancy.status = request_status
    vacancy.moderator = CustomUser.objects.get(pk=user_id)
    vacancy.save()

    serializer = VacancySerializer(vacancy, many=False)
    return Response(serializer.data)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_vacancy(request, vacancy_id):
    """
    Удаляет вакансию
    """
    if not Vacancy.objects.filter(pk=vacancy_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    vacancy = Vacancy.objects.get(pk=vacancy_id)

    if vacancy.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    vacancy.status = 5
    vacancy.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
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


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token
    }

    response = Response(user_data, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=access_token_lifetime)

    return response


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    message = {
        'message': 'User registered successfully',
        'user_id': user.id,
        "access_token": access_token
    }

    response = Response(message, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=access_token_lifetime)

    return response


@api_view(["POST"])
def check(request):
    token = get_access_token(request)

    if token is None:
        message = {"message": "Token is not found"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    if token in cache:
        message = {"message": "Token in blacklist"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    user = CustomUser.objects.get(pk=user_id)
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, access_token_lifetime)

    message = {"message": "Вы успешно вышли из аккаунта"}
    response = Response(message, status=status.HTTP_200_OK)

    response.delete_cookie('access_token')

    return response
