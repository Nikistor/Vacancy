"""
URL configuration for bmstu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from bmstu_lab import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    # Панель админа
    path('admin/', admin.site.urls),

    # Включим URL-пути для вашего API через include
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # УСЛУГА (Город)
    # Услуги - список, одна запись, добавление, изменение, удаление, добавление в заявку
    path(r'city/', views.CityList.as_view(), name='city-list'),
    path(r'city/<int:pk>/', views.CityDetail.as_view(), name='city-detail'),
    path(r'city/<int:pk>/update/', views.put_city_detail, name='city-put'),

    # ЗАЯВКА (Вакансия)
    # Заявки - список, одна запись, изменение, статусы создателя, статусы модератора, удаление
    path(r'vacancy/', views.VacancyList.as_view(), name='vacancy-list'),
    path(r'vacancy/<int:pk>/', views.VacancyDetail.as_view(), name='vacancy-detail'),
    path(r'vacancy/<int:pk>/update/', views.put_vacancy_detail, name='vacancy-put'),
    path(r'vacancy/<int:pk>/update_by_employer/', views.put_vacancy_BY_EMPLOYER, name='vacancy-put'),
    path(r'vacancy/<int:pk>/update_by_moderator/', views.put_vacancy_BY_MODERATOR, name='vacancy-put'),

    # М-М (Вакансии города)
    # м-м - удаление из заявки, изменение количества/значения в м-м
    path(r'vacancycity/', views.VacancyCityList.as_view(), name='vacancycity-list'),
    path(r'vacancycity/<int:pk>/', views.VacancyCityDetail.as_view(), name='vacancycity-detail'),
]
