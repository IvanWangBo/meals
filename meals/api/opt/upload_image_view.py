# coding=utf=8
import hashlib
import os

from api.base_view import HttpApiBaseView
from django.core.files.uploadedfile import UploadedFile
from rest_framework.request import Request
from rest_framework.response import Response
from serializers import UploadImageSerializer
from settings import UPLOAD_ROOT


class UploadImageView(HttpApiBaseView):
    base_path = UPLOAD_ROOT

    def _post_data(self, request):
        # type: (Request) -> Response
        serializer = UploadImageSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            image = data.get('image')
            path = self.save(image)
            return self.success_response({'path': path, 'url_suffix': '/static/' + path})
        return self.error_response({}, u"无效图片")

    def read_file_content(self, file):
        # type: (UploadedFile) -> []bytes
        file.open("rb")
        content = file.read()
        file.close()
        return content

    def md5(self, content):
        md5 = hashlib.md5()
        md5.update(content)
        return md5.hexdigest()

    def get_md5_name(self, file_name, content):
        ext = file_name.split('.')[-1]
        file_md5 = self.md5(content)
        return '%s/%s.%s' % (file_md5[:2], file_md5[2:], ext)

    def save(self, image):
        # type: (UploadedFile) -> str
        content = self.read_file_content(image)
        file_name = self.get_md5_name(image.name, content)
        target_path = os.path.join(self.base_path, file_name)
        target_dir = os.path.dirname(target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        with open(target_path, 'wb+') as target:
            target.write(content)
        return file_name

