from django.db import models

from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    """
    Модель курса
    """

    name = models.CharField(max_length=50, verbose_name="course name")
    preview = models.ImageField(
        verbose_name="preview",
        upload_to="images/materials/course",
        null=True,
        blank=True,
    )
    description = models.TextField(verbose_name="description")
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    Модель урока
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    name = models.CharField(max_length=50, verbose_name="lesson name")
    description = models.TextField(verbose_name="description")
    preview = models.ImageField(
        verbose_name="preview",
        upload_to="images/materials/lesson",
        null=True,
        blank=True,
    )
    video_url = models.URLField(blank=True, null=True, verbose_name="Video URL")
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lessons",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """
    Модель подписки
    """

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="subscriptions"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ["user"]
