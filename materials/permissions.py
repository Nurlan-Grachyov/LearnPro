import logging

from rest_framework.permissions import BasePermission

logging.basicConfig(level=logging.DEBUG)


class Moderators(BasePermission):
    """
    Проверка на права доступа. Вернет True, если пользователь superuser или входит в группу Moderators
    """

    def has_permission(self, request, view):
        if request.method in ("GET", "PUT", "PATCH"):
            return (
                request.user.groups.filter(name="Moderators").exists()
                or request.user.is_superuser
            )
        elif request.method == "POST":
            return request.user.is_superuser
        return False


class Owner(BasePermission):
    """
    Проверка на права доступа. Вернет True, если пользователь, совершающий операцию, является владельцем объекта
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "PUT", "PATCH", "DELETE"):
            logging.debug("good2")
            return request.user == obj.owner
        return False
