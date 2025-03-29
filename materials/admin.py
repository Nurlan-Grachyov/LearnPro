from django.contrib import admin

from materials.models import Course, Lesson

admin.site.register(Lesson)
admin.site.register(Course)
