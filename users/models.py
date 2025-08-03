from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=35, verbose_name="Ник пользователя", unique=True
    )
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=35, blank=True, null=True)
    avatar = models.ImageField(
        verbose_name="Аватар", null=True, blank=True, upload_to="users_avatar/"
    )
    telegram_id = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Telegram ID"
    )
    telegram_chat_id = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Telegram Chat ID"
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
