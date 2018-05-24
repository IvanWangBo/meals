# coding=utf-8
from rest_framework import serializers
from datetime import datetime


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)


class UserListSerializer(serializers.Serializer):
    company_id = serializers.IntegerField(allow_null=False)


class AddPersonnelSerializer(serializers.Serializer):
    company_id = serializers.IntegerField(allow_null=False)
    user_name = serializers.CharField(max_length=30, allow_blank=False)
    real_name = serializers.CharField(max_length=30, allow_blank=False)
    password = serializers.CharField(max_length=30, allow_blank=False)
    email = serializers.CharField(max_length=254, allow_blank=False)
    department_id = serializers.IntegerField(allow_null=False)
    gender = serializers.IntegerField(allow_null=False)
    phone_number = serializers.CharField(max_length=30, allow_blank=True)


class ResetUserSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=30, allow_blank=False)
    new_password = serializers.CharField(max_length=30, allow_blank=False)

class MealsOrderSerializer(serializers.Serializer):
    order_list = serializers.CharField(max_length=1024, allow_blank=False)
    time_range = serializers.IntegerField(allow_null=False)


class CancelMealsOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(allow_null=False)


class MealsOrderListSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(allow_null=True, default=-9)
    year = serializers.IntegerField(allow_null=True, default=datetime.now().month)
    month = serializers.IntegerField(allow_null=True, default=datetime.now().month)
    status = serializers.IntegerField(allow_null=True, default=-9)
