from bmstu_lab.models import Users
from django.core.management import BaseCommand


def add_users():
    Users.objects.create_user("user1", "1234", False)
    Users.objects.create_superuser("root", "1234", True)

    print("Пользователи созданы")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()