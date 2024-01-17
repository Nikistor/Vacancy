from django.core.management.base import BaseCommand
from vacancies.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        City.objects.all().delete()
        Vacancy.objects.all().delete()
        CustomUser.objects.all().delete()