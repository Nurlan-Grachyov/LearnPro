from rest_framework.permissions import BasePermission

from users.models import CustomUser


class SelfUser(BasePermission):
    """
    Проверка на права доступа. Вернет True, если пользователь является владельцем аккаунта
    """

    def has_object_permission(self, request, view, obj):
        user = CustomUser.objects.get(email=obj)
        if request.method in ("GET", "PUT", "PATCH", "DELETE"):
            return request.user == user
        return False
