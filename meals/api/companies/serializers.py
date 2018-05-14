# coding=utf-8
from rest_framework import serializers


class AddCompanySerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=30, allow_blank=False)
    province = serializers.CharField(max_length=30, allow_blank=False)
    address = serializers.CharField(max_length=256, allow_blank=False)
    phone_number = serializers.CharField(max_length=30, allow_blank=False)


class AddCompanyAdminSerializer(serializers.Serializer):
    company_id = serializers.IntegerField(allow_null=False)
    admin_name = serializers.CharField(max_length=30, allow_blank=False)
    password = serializers.CharField(max_length=30, allow_blank=False)


class ResetCompanyAdminSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(allow_null=False)
    password = serializers.CharField(max_length=30, allow_blank=False)