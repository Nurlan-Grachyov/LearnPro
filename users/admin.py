from django.contrib import admin

from users.models import CustomUser, Payments

admin.site.register(CustomUser)
admin.site.register(Payments)
