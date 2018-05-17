# coding=utf-8
from django.http import HttpResponse
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.views import Response


class HttpApiBaseView(APIView):

    def success_response(self, data, message=""):
        return Response(data={"code": 200, "data": data, "message": message})

    def error_response(self, data, message=""):
        return Response(data={"code": 400, "data": data, "message": message})

    def serializer_invalid_response(self, serializer):
        messages = ""
        for k, v in serializer.errors.iteritems():
            messages += "%s : %s\n" % (k, v[0])
        return self.error_response({}, message=messages)
