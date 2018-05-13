# coding=utf-8
from rest_framework import serializers


class AddCompanySerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=30, allow_blank=False)
    province = serializers.CharField(max_length=30, allow_blank=False)
    address = serializers.CharField(max_length=256, allow_blank=False)
