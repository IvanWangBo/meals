# coding=utf8

from rest_framework import serializers
from django.core.files.uploadedfile import UploadedFile


class UploadImageSerializer(serializers.Serializer):
    image = serializers.ImageField(allow_empty_file=False, use_url=False, write_only=True)

    def create(self, validated_data):
        # type: (UploadedFile) -> None
        print validated_data

