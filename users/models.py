from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError

from materials.models import Course, Lesson


class CustomUser(AbstractUser):
    """
    Модель пользователя
    """

    username = models.CharField(null=True, blank=True, verbose_name="username")
    first_name = models.CharField(null=True, blank=True, verbose_name="first_name")
    last_name = models.CharField(null=True, blank=True, verbose_name="last_name")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = PhoneNumberField(
        blank=True, null=True, verbose_name="Phone number", unique=True
    )
    town = models.CharField(blank=True, null=True, verbose_name="town")
    avatar = models.ImageField(
        blank=True, null=True, verbose_name="avatar", upload_to="images/users"
    )
    is_staff = models.BooleanField(blank=True, default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Product(models.Model):
    """
    Модель продукта
    """

    name = models.CharField(verbose_name="продукт", max_length=50)
    stripe_id = models.CharField(verbose_name="идентификатор продукта")
    paid_course = ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="paid_course",
        null=True,
        blank=True,
    )
    paid_lesson = ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="paid_lesson",
        null=True,
        blank=True,
    )

    def clean(self):
        """
        Переопределение метода clean, проверяющий, что указан предмет оплаты
        """

        super().clean()
        if not self.paid_course and not self.paid_lesson:
            raise ValidationError(
                "Должен быть указан либо оплаченный курс, либо оплаченный урок."
            )

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"


class Payments(models.Model):
    """
    Модель платежей
    """

    CASH = "cash"
    PAYMENT_TRANSFER = "payment_transfer"

    STATUS_IN_CHOICES = [
        (CASH, "оплата наличными"),
        (PAYMENT_TRANSFER, "оплата переводом"),
    ]

    user = ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user")
    pay_date = models.DateField(
        verbose_name="дата оплаты", auto_now_add=True, blank=True
    )
    paid_course = ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="paid_course",
        null=True,
        blank=True,
    )
    paid_lesson = ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="paid_lesson",
        null=True,
        blank=True,
    )
    payment_amount = models.FloatField(verbose_name="сумма оплаты")
    payment_method = models.CharField(
        choices=STATUS_IN_CHOICES, max_length=16, verbose_name="способ оплаты"
    )

    def clean(self):
        """
        Переопределение метода clean, проверяющий, что указан предмет оплаты
        """

        super().clean()
        if not self.paid_course and not self.paid_lesson:
            raise ValidationError(
                "Должен быть указан либо оплаченный курс, либо оплаченный урок."
            )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплата"

    def __str__(self):
        return f"Вы оплатили {'курс ' + str(self.paid_course.name) if self.paid_course else 'урок ' + str(self.paid_lesson.name)} на сумму {self.payment_amount}"
