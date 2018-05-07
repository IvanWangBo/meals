# coding=utf-8
from django.db import models


class Companies(models.Model):
    company_name = models.CharField(max_length=30, blank=False)
    phone_number = models.CharField(max_length=254, blank=False, null=True)
    address = models.CharField(max_length=256, blank=True)
    is_enabled = models.BooleanField(default=True, blank=False)
    create_time = models.DateTimeField(auto_now_add=True, blank=False)

    class Meta:
        db_table = "companies"

class Departments(models.Model):
    name = models.CharField(max_length=128, blank=False, default='')
    company_id = models.IntegerField(default=0, blank=False)
    create_time = models.DateTimeField(auto_now_add=True, blank=False)

    class Meta:
        db_table = "departments"
