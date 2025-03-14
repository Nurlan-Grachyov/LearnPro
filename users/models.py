from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = models.CharField(null=True, blank=True, verbose_name="username")
    first_name = models.CharField(null=True, blank=True, verbose_name="first_name")
    last_name = models.CharField(null=True, blank=True, verbose_name="last_name")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name="Phone number")
    town = models.CharField(blank=True, null=True, verbose_name="town")
    avatar = models.ImageField(blank=True, null=True, verbose_name="avatar", upload_to="images/users")

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
