# coding=utf-8
from django.http import HttpResponse
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.views import Response


class HttpApiBaseView(APIView):

    def success_response(self, data):
        return Response(data={"code": 0, "data": data})

    def error_response(self, error_reason):
        return Response(data={"code": 1, "data": error_reason})

    def serializer_invalid_response(self, serializer):
        for k, v in serializer.errors.iteritems():
            return self.error_response(k + " : " + v[0])
