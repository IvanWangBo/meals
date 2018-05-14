# coding=utf-8
from django.db import models

class Restaurants(models.Model):
    name = models.CharField(max_length=30, blank=False)
    phone_number = models.CharField(max_length=254, blank=False, null=True)
    address = models.CharField(max_length=256, blank=True)
    is_enabled = models.IntegerField(default=True, blank=False)
    create_time = models.DateTimeField(auto_now_add=True, blank=False)


    class Meta:
        db_table = "restaurants"

class Dishes(models.Model):
    name = models.CharField(max_length=128, blank=False)
    price = models.FloatField()
    restaurant_id = models.IntegerField(default=0, blank=False)
    image_url = models.CharField(max_length=256, blank=False, default='')
    support_times = models.CharField(default='', blank=False, max_length=256)
    create_time = models.DateTimeField(auto_now_add=True, blank=False)

    class Meta:
        db_table = 'dishes'


class TimeRange(models.Model):
    name = models.CharField(max_length=30, blank=False)
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)
    create_time = models.DateTimeField(auto_now_add=True, blank=False)

    class Meta:
        db_table = 'time_range'

