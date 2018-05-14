# coding=utf-8
from django.db import models


class Companies(models.Model):
    company_name = models.CharField(max_length=128, blank=False)
    province = models.CharField(max_length=30, blank=False, default='Beijing')
    address = models.CharField(max_length=256, blank=False, default='')
    is_enabled = models.IntegerField(default=1, blank=False)
    create_time = models.DateTimeField(auto_now_add=True, blank=False)

    class Meta:
        db_table = "companies"

class Departments(models.Model):
    name = models.CharField(max_length=128, blank=False, default='')
    company_id = models.IntegerField(default=0, blank=False)
    create_time = models.DateTimeField(auto_now_add=True, blank=False)

    class Meta:
        db_table = "departments"


class RestaurantRelation(models.Model):
    company_id = models.IntegerField(default=0, blank=False)
    restaurant_id = models.IntegerField(default=0, blank=False)
    is_enabled = models.IntegerField(default=0, blank=False)
    create_time = models.DateTimeField(auto_now_add=True, blank=False)

    class Meta:
        db_table = "restaurant_relation"

