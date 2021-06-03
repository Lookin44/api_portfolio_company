from django.contrib.auth.models import AbstractUser
from django.db import models


class RoleUser(models.TextChoices):
    USER = 'user'
    ADMIN = 'admin'


class User(AbstractUser):

    username = models.CharField(max_length=50, unique=True, blank=False)
    role = models.CharField(
        max_length=10,
        choices=RoleUser.choices,
        default=RoleUser.USER
    )

    @property
    def is_admin(self):
        return (self.role == RoleUser.ADMIN or self.is_staff
                or self.is_superuser)
