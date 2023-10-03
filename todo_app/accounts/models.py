from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models

from todo_app.accounts.validators import (validate_name_contains_valid_symbols_and_numbers,
                                          validate_password_is_strong)


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)


class Account(AbstractBaseUser, models.Model):
    MAX_LEN_USERNAME = 30
    MIN_LEN_USERNAME = 4

    MAX_LEN_PASSWORD = 128
    MIN_LEN_PASSWORD = 8

    username = models.CharField(max_length=MAX_LEN_USERNAME,
                                validators=[MinLengthValidator(MIN_LEN_USERNAME),
                                            validate_name_contains_valid_symbols_and_numbers],
                                unique=True,
                                null=False, blank=False)

    password = models.CharField(max_length=MAX_LEN_PASSWORD,
                                validators=[MinLengthValidator(MIN_LEN_PASSWORD),
                                            validate_password_is_strong],
                                null=False, blank=False)

    repeated_password = models.CharField(max_length=MAX_LEN_PASSWORD,
                                         null=False, blank=False)

    is_staff = models.BooleanField(default=False)

    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()
    USERNAME_FIELD = 'username'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, accounts):
        return self.is_superuser

    def __str__(self):
        return self.username

    def clean(self):
        if self.repeated_password != self.password:
            raise ValidationError("Password doesn't match.")
