# coding=utf-8
from rest_framework import serializers


class AddDishSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30, allow_blank=False)
    price = serializers.FloatField(allow_null=False)
    restaurant_id = serializers.IntegerField(allow_null=False)
    image_url = serializers.CharField(max_length=30, allow_null=False)
    support_times = serializers.CharField(max_length=128, allow_blank=False)


class AddTimeRangeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30, allow_blank=False)
    start_time = serializers.TimeField(allow_null=False)
    end_time = serializers.TimeField(allow_null=False)


class DishesListSerializer(serializers.Serializer):
    restaurant_id = serializers.IntegerField(allow_null=False)
    time_range_id = serializers.IntegerField(allow_null=False)


class ModifyTimeRangeSerializer(serializers.Serializer):
    dish_id = serializers.IntegerField(allow_null=False)
    time_range_id = serializers.IntegerField(allow_null=False)


class AddRestaurantSerializer(serializers.Serializer):
    restaurant_name = serializers.CharField(max_length=30, allow_blank=False)
    phone_number = serializers.CharField(max_length=254, allow_blank=False)
    address = serializers.CharField(max_length=256, allow_blank=False)


class DeleteRestaurantSerializer(serializers.Serializer):
    restaurant_id = serializers.IntegerField(allow_null=False)


class DeleteDishSerializer(serializers.Serializer):
    dish_id = serializers.IntegerField(allow_null=False)
