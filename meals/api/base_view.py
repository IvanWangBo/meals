# coding=utf-8
from django.http import HttpResponse
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.views import Response
from common.exceptions import RequestBaseException

from api.users.models import Users


class HttpApiBaseView(APIView):

    def success_response(self, data, message=u""):
        return Response(data={"code": 200, "data": data, "message": message})

    def error_response(self, data, message=u""):
        return Response(data={"code": 400, "data": data, "message": message})

    def serializer_invalid_response(self, serializer):
        messages = ""
        for k, v in serializer.errors.iteritems():
            messages += "%s : %s\n" % (k, v[0])
        return self.error_response({}, message=messages)

    def get_login_user_id(self, request):
        return request.user.id

    def get_login_user_company_id(self, request):
        return request.user.company_id

    def check_user_company(self, user_id, company_id):
        user = Users.objects.get(id=user_id)
        if user.company_id != company_id:
            self.error_response({}, message=u"对不起，您查询的公司有误！")

    def post(self, *args, **kwargs):
        try:
            return self._post_data(*args, **kwargs)
        except RequestBaseException as e:
            return e.json_response()
