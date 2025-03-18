from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()
        user = User.objects.create(email="nurlan_admin@mail.ru", is_active=True)
        user.set_password("12345678")
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        self.stdout.write("It was successfully created")
# normal@mail.ru
# nurlan@mail.ru
# moderator@mail.ru
# nurlan_admin@mail.ru