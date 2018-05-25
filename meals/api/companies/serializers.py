# coding=utf-8
from datetime import datetime
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
    password = serializers.CharField(max_length=30, allow_blank=False)


class AddDepartmentSerializer(serializers.Serializer):
    department_name = serializers.CharField(max_length=30, allow_blank=False)
    company_id = serializers.IntegerField(allow_null=False)


class RestaurantOrdersSummarySerializer(serializers.Serializer):
    month = serializers.IntegerField(allow_null=True, default=datetime.now().month)
    year = serializers.IntegerField(allow_null=True, default=datetime.now().year)


class RestaurantOrdersDetailsSerializer(serializers.Serializer):
    year = serializers.IntegerField(allow_null=True, default=datetime.now().year)
    month = serializers.IntegerField(allow_null=True, default=datetime.now().month)
    restaurant_id = serializers.IntegerField(allow_null=False)
