from django.contrib import admin

from .models import City, Vacancy, Users, VacancyCity

admin.site.register(City)
admin.site.register(Vacancy)
admin.site.register(Users)
admin.site.register(VacancyCity)
