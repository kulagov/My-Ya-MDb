from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    MODERATOR = 'moderator'
    USER_ROLE = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    ]

    email = models.EmailField('email address', unique=True)

    role = models.CharField(
        max_length=30,
        choices=USER_ROLE,
        default=USER,
        db_column='role')

    description = models.CharField(blank=True, max_length=30)

    bio = models.CharField(blank=True, max_length=200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def is_admin(self):
        return bool(self.is_superuser or self.role == self.ADMIN)

    @property
    def is_moderator(self):
        return bool(self.role == self.MODERATOR)

    @property
    def is_user(self):
        return bool(self.role == self.USER)

    def __str__(self):
        return self.email
