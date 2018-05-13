# coding=utf-8
from rest_framework import serializers


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
    user_id = serializers.IntegerField(allow_null=False)
    password = serializers.CharField(max_length=30, allow_blank=False)
    new_password = serializers.CharField(max_length=30, allow_blank=False)

