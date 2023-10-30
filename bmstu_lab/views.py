from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from bmstu_lab.serializers import CitySerializer, VacancySerializer, VacancyCitySerializer, UsersSerializer
from bmstu_lab.models import City, Vacancy, VacancyCity, Users
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from bmstu_lab.DB_Minio import DB_Minio
from datetime import datetime
from PIL import Image
import io
import requests
from rest_framework import generics
from django.utils import timezone

# Город
class CityList(APIView):
    model_class = City
    serializer_class = CitySerializer

    def get(self, request, format=None):
        """
        Возвращает список городов
        """

        # Получим параметры запроса из URL
        name = request.GET.get('name')
        foundation_date = request.GET.get('foundation_date')
        grp = request.GET.get('grp')
        climate = request.GET.get('climate')
        square = request.GET.get('square')
        status = request.GET.get('status')
        description = request.GET.get('description')

        # Получение данные после запроса с БД (через ORM)
        city = self.model_class.objects.all()

        if name and foundation_date and grp and climate and square and status and description is None:
            pass
        else:
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
            if status:
                city = city.filter(status=status)
            if description:
                city = city.filter(description__icontains=description)

        serializer = self.serializer_class(city, many=True)
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

    def put(self, request, pk, format=None):
        """
        Обновляет информацию о городе
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
        if not self.model_class.objects.filter(pk=pk).exists():
            return Response(f"ERROR! There is no such object!")

        city = get_object_or_404(self.model_class, pk=pk)
        city.delete()
        return Response('Successfully deleted', status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def GET_city(request, pk=None, format=None):
    """
    Возвращает информацию о конкретном городе
    """
    if request.method == 'GET':
        city = get_object_or_404(City, pk=pk)

    serializer = CitySerializer(city)
    return Response(serializer.data)

def process_image_from_url(feature, url_photo):
    if url_photo:
        DB = DB_Minio()
        DB.put_object_url(bucket_name='vacancy_city', object_name=feature+'.jpg', url=url_photo)
        # Загрузите данные по URL
        response = requests.get(url_photo)
        if response.status_code == 200:
            # Возврат данных в бинарном виде (в байтах)
            image_data = response.content

            # Используйте Pillow для обработки изображения и сохранения его в формате JPEG
            try:
                image = Image.open(io.BytesIO(image_data))
                image = image.convert('RGB')  # Преобразование изображения в формат RGB
                output_buffer = io.BytesIO()
                image.save(output_buffer, format='JPEG')
                jpeg_data = output_buffer.getvalue()
                return jpeg_data
            except Exception as ex:
                return None  # Возвращаем None в случае ошибки при обработке изображения
        else:
            return None  # Возвращаем None в случае ошибки при получении изображения по URL
    else:
        # Если нет URL изображения, возвращаем None
        return None

# Добавляет новую запись в заявку
@api_view(['POST'])
def POST_city_in_vacancy(request, pk, format=None):
    try:
        city = City.objects.get(pk=pk)
    except City.DoesNotExist:
        return Response(f"ERROR! Object City does not exist with ID {pk}",
                        status=status.HTTP_404_NOT_FOUND)

    # Находим заявку с таким статусом
    vacancy = Vacancy.objects.filter(status_vacancy='Создана').last()
    # Если такой заявки нет, то создаем
    if vacancy == None:
        # status_vacancy [Закрыта, Опубликована, Создана, Отклонена, На модерации]

        vacancy = Vacancy.objects.create(
            date_create=datetime.now(),
            status_vacancy='Создана',
        )

    # Создание записи в таблице VacancyCity для связи между Vacancy и City
    VacancyCity.objects.create(
        id_city=city,
        id_vacancy=vacancy,
    )
    return Response(f'Successfully created, vacancy ID: {vacancy.id}', status=status.HTTP_201_CREATED)

# Вакансия
class VacancyList(APIView):
    model_class = Vacancy
    serializer_class = VacancySerializer

    def get(self, request, format=None):
        """
        Возвращает список вакансий
        """
        vacancy = Vacancy.objects.all()

        # Получим параметры запроса из URL
        name_vacancy = request.GET.get('name_vacancy')
        status_vacancy = request.GET.get('status_vacancy')
        date_create = request.GET.get('date_create')
        date_close = request.GET.get('date_close')
        # Дата после
        date_form_after = request.GET.get('date_form_after')
        # Дата ДО
        date_form_before = request.GET.get('date_form_before')

        # Проверяет, пустой запрос на фильтр
        if all(item is None for item in
               [name_vacancy, status_vacancy, date_create, date_close, date_form_after, date_form_before]):
            # Сериализиуем его, чтобы получить в формате JSON
            vacancy_serializer = self.serializer_class(vacancy, many=True)
        else:
            # Применим фильтры на основе параметров запроса, если они предоставлены
            if name_vacancy:
                vacancy = vacancy.filter(name_vacancy=name_vacancy)
            if status_vacancy:
                vacancy = vacancy.filter(status_vacancy=status_vacancy)
            if date_create:
                vacancy = vacancy.filter(date_create=date_create)
            if date_close:
                vacancy = vacancy.filter(date_close=date_close)

            # Дата формирования ПОСЛЕ
            if date_form_after and date_form_before is None:
                vacancy = vacancy.filter(date_form__gte=date_form_after)
            # Дата формирования ДО
            if date_form_after is None and date_form_before:
                vacancy = vacancy.filter(date_form__lte=date_form_before)

            # Дата формирования ПОСЛЕ и ДО
            if date_form_after and date_form_before:
                if date_form_after > date_form_before:
                    return Response('Mistake! It is impossible to sort when "BEFORE" exceeds "AFTER"!')
                vacancy = vacancy.filter(date_form__gte=date_form_after)
                vacancy = vacancy.filter(date_form__lte=date_form_before)

            # Сериализуем результаты запроса
            vacancy_serializer = VacancySerializer(vacancy, many=True)

        return Response(vacancy_serializer.data)

    def post(self, request, format=None):
        """
        Добавляет новую запись
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        """
        Обновляет информацию о вакансии
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
        if not self.model_class.objects.filter(pk=pk).exists():
            return Response(f"ERROR! There is no such object!")

        vacancy = get_object_or_404(self.model_class, pk=pk)
        vacancy.delete()
        return Response('Successfully deleted', status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def GET_vacancy(request, pk=None, format=None):
    """
    Возвращает информацию о конкретном вакансии
    """
    if request.method == 'GET':
        try:
            vacancy = get_object_or_404(Vacancy, pk=pk)
        except Vacancy.DoesNotExist:
            return Response({"error": "Vacancy not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            moderator = get_object_or_404(Users, id=vacancy.id_moderator.id)
        except Users.DoesNotExist:
            moderator = None  # Модератор не найден, устанавливаем moderator в None

        try:
            employer = get_object_or_404(Users, id=vacancy.id_employer.id)
        except Users.DoesNotExist:
            employer = None  # Работодатель не найден, устанавливаем employer в None

        vacancycities = VacancyCity.objects.filter(id_vacancy=vacancy.id)
        city_serializer = []

        for vacancycity in vacancycities:
            try:
                city = get_object_or_404(City, id=vacancycity.id_city.id)
                city_serializer.append(CitySerializer(city).data)
            except City.DoesNotExist:
                city_serializer.append({"error": "City not found"})

        response = {
            "moderator": UsersSerializer(moderator).data,
            "employer": UsersSerializer(employer).data,
            "vacancy": VacancySerializer(vacancy).data,
            "city": city_serializer
        }

        return Response(response)

# @api_view(['PUT'])
# def PUT_vacancy(request, pk, format=None):
#     """
#     Обновляет информацию о вакансии
#     """
#     vacancy = get_object_or_404(Vacancy, pk=pk)
#     vacancy_serializer = VacancySerializer(vacancy, data=request.data, partial=True)
#     if vacancy_serializer.is_valid():
#         vacancy_serializer.save()
#         return Response(vacancy_serializer.data)
#     return Response(vacancy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def PUT_vacancy_BY_EMPLOYER(request, pk, format=None):
    """
    Обновляет информацию о вакансии
    """
    if request.data['status_vacancy'] in ['Создана', 'Закрыта']:
        try:
            vacancy = Vacancy.objects.get(pk=pk)
        except Vacancy.DoesNotExist:
            return Response("Vacancy not found", status=status.HTTP_404_NOT_FOUND)

        vacancy.status_vacancy = request.data['status_vacancy']

        if 'id_employer' in request.data:
            new_id_employer = request.data['id_employer']
            try:
                new_employer = Users.objects.get(pk=new_id_employer)
                vacancy.id_employer = new_employer
                vacancy.save()
                return Response("Successfully updated status")
            except Users.DoesNotExist:
                return Response("New employer not found", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response('You are not moderator! Check status in [Создана, Закрыта]')

@api_view(['PUT'])
def PUT_vacancy_BY_MODERATOR(request, pk, format=None):
    """
    Обновляет информацию о вакансии
    """
    if request.data['status_vacancy'] in ['На модерации', 'Закрыта', 'Опубликована', 'Отклонена']:
        try:
            vacancy = Vacancy.objects.get(pk=pk)
        except Vacancy.DoesNotExist:
            return Response("Vacancy not found", status=status.HTTP_404_NOT_FOUND)

        vacancy.status_vacancy = request.data['status_vacancy']

        if 'id_moderator' in request.data:
            new_id_moderator = request.data['id_moderator']
            try:
                new_moderator = Users.objects.get(pk=new_id_moderator)
                vacancy.id_moderator = new_moderator
                vacancy.save()
                return Response("Successfully updated status")
            except Users.DoesNotExist:
                return Response("New moderator not found", status=status.HTTP_404_NOT_FOUND)
        # return Response(mars_station_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('You are not moderator! Check status in [На модерации, Закрыта, Опубликована, Отклонена]')

# Вакансии города
class VacancyCityList(APIView):
    model_class = VacancyCity
    serializer_class = VacancyCitySerializer

    def put(self, request, pk, format=None):
        """
        Обновляет информацию о вакансии города
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
        # Удаляет связанную вакансию
        vacancycity.id_vacancy.delete()
        # Затем удалим сам объект VacancyCity
        vacancycity.delete()
        return Response('Successfully deleted', status=status.HTTP_204_NO_CONTENT)