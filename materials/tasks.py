from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from users.models import CustomUser


# @shared_task
def send_email_about_update_materials(users_ids):
    users = []
    for user_id in users_ids:
        user = CustomUser.objects.get(id=user_id)
        print(user)
        print(user.last_login)
        users.append(user.email)
    send_mail(
        "Материалы обновлены",
        "Получены обновления материалов, скорее смотрите",
        EMAIL_HOST_USER,
        users,
    )
@shared_task
def block():
    users = CustomUser.objects.all()
    for user in users:
        if timezone.now() - user.last_login > timezone.timedelta(days=30):
            user.is_active = False