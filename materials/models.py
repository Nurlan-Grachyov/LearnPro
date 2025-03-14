from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='course name')
    preview = models.ImageField(verbose_name="preview", upload_to='images/materials/course', null=True, blank=True)
    description = models.TextField(verbose_name="description")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=50, verbose_name='lesson name')
    description = models.TextField(verbose_name="description")
    preview = models.ImageField(verbose_name="preview", upload_to='images/materials/lesson', null=True, blank=True)
    video_url = models.URLField(blank=True, null=True, verbose_name="Video URL")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["name"]
