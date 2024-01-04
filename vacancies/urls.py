from django.urls import path

from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/cities/search/', search_city),  # GET
    path('api/cities/<int:city_id>/', get_city_by_id),  # GET
    path('api/cities/<int:city_id>/update/', update_city),  # PUT
    path('api/cities/<int:city_id>/delete/', delete_city),  # DELETE
    path('api/cities/create/', create_city),  # POST
    path('api/cities/<int:city_id>/add_to_vacancy/', add_city_to_vacancy),  # POST
    path('api/cities/<int:city_id>/image/', get_city_image),  # GET
    path('api/cities/<int:city_id>/update_image/', update_city_image),  # PUT

    # Набор методов для заявок
    path('api/vacancies/search/', get_vacancies),  # GET
    path('api/vacancies/<int:vacancy_id>/', get_vacancy_by_id),  # GET
    path('api/vacancies/<int:vacancy_id>/update/', update_vacancy),  # PUT
    path('api/vacancies/<int:vacancy_id>/update_bankrupt/', update_vacancy_bankrupt),  # POST
    path('api/vacancies/<int:vacancy_id>/update_status_user/', update_status_user),  # PUT
    path('api/vacancies/<int:vacancy_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/vacancies/<int:vacancy_id>/delete/', delete_vacancy),  # DELETE
    path('api/vacancies/<int:vacancy_id>/delete_city/<int:city_id>/', delete_city_from_vacancy),  # DELETE

    # Набор методов для аутентификации и авторизации
    path("api/register/", register),
    path("api/login/", login),
    path("api/check/", check),
    path("api/logout/", logout)
]