from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Класс создания суперюзера
    """

    def handle(self, *args, **kwargs):
        User = get_user_model()
        user = User.objects.create(email="nurlan-admin@mail.ru")
        user.set_password("12345678")
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        self.stdout.write("It was successfully created")
