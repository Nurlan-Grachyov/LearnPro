import logging

from rest_framework.permissions import BasePermission

logging.basicConfig(level=logging.DEBUG)


class Moderators(BasePermission):
    def has_permission(self, request, view):
        logging.debug("good5")
        if request.method in ("GET", "PUT", "PATCH"):
            logging.debug("good6")
            return (
                request.user.groups.filter(name="Moderators").exists()
                or request.user.is_superuser
            )
        elif request.method == "POST":
            logging.debug("good7")
            return request.user.is_superuser
        return False


class Owner(BasePermission):
    def has_object_permission(self, request, view, obj):
        logging.debug("good")
        if request.method in ("GET", "PUT", "PATCH", "DELETE"):
            logging.debug("good2")
            return request.user == obj.owner
        logging.debug("good4")
        return False
