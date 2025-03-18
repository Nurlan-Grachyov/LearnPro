from rest_framework.permissions import BasePermission


class Moderators(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "PUT", "PATCH"):
            return request.user.groups.filter(name='Moderators').exists()
        return False

