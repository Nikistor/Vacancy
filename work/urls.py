
from django.contrib import admin
from django.urls import path

from vacancies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Список городов (Фильтрация)
    path('', views.GetCities, name='cities'),
    # Сведения о городе
    path('city/<int:id>/', views.GetCity, name='url_city'),
    # Удаление города
    path('delete_city/', views.DeleteCityByID, name='delete_city'),
]
