from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class PersonManager(BaseUserManager):
    def create_user(self, username, email, role, password=None):
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            role = role,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_super_user(self, username, email, role, password):
        user = self.create_user(
            username,
            email,
            role,
            password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user

class Person(AbstractBaseUser):
    # Unique fields
    username = models.CharField(max_length=50, unique=True, default='')
    USERNAME_FIELD = 'username'

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        default=''
    )

    # Other Fields
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")

    # Roles and permissions
    PROFESSOR = 'PRO'
    GENERAL = 'GEN'

    ROLE_CHOICE = (
        (PROFESSOR, 'Professor'),
        (GENERAL, 'General'),
    )

    role = models.CharField(max_length=3, choices=ROLE_CHOICE, default=GENERAL)

    is_admin = models.BooleanField(default=False)

    #
    objects = PersonManager()

    def __str__(self):
        return self.username


