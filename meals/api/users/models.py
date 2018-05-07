# coding=utf-8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from common.constants import UserGender
from common.constants import UserAdminType


class UserManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, user_name):
        return self.get(**{self.model.USERNAME_FIELD: user_name})


class Users(AbstractBaseUser):
    user_name = models.CharField(max_length=30, unique=True, blank=False)
    real_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(max_length=254, blank=True)
    admin_type = models.IntegerField(default=UserAdminType.personnel)
    phone_number = models.CharField(max_length=20, blank=False)
    gender = models.IntegerField(default=UserGender.unknown)
    company_id = models.IntegerField(default=0, blank=False)
    department_id = models.IntegerField(default=0, blank=False, choices=[])
    is_enabled = models.BooleanField(default=True, blank=False)
    create_time = models.DateTimeField(auto_now_add=True, blank=False)

    USERNAME_FIELD = 'user_name'

    objects = UserManager()

    class Meta:
        db_table = "users"
