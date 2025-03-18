import logging

from rest_framework.permissions import BasePermission

logging.basicConfig(level=logging.DEBUG)


class Moderators(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "PUT", "PATCH"):
            if request.user.groups.filter(name='Moderators').exists() or request.user.is_superuser:
                return True
        return False


class Owner(BasePermission):
    def has_object_permission(self, request, view, obj):
        logging.debug("good")
        if request.method in ("GET", "PUT", "PATCH", "DELETE"):
            logging.debug("good2")
            if request.user == obj.owner:
                logging.debug("good3")
                return True
        logging.debug("good4")
        return False
