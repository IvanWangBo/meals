# coding=utf-8
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)
