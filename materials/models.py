from django.db import models


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name='course name')
    description = models.TextField(verbose_name="description")
    preview = models.ImageField(verbose_name="preview", upload_to='images/materials/lesson')
    video_url = models.URLField(blank=True, null=True, verbose_name="Video URL")


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='course name')
    preview = models.ImageField(verbose_name="preview", upload_to='images/materials/course')
    description = models.TextField(verbose_name="description")
