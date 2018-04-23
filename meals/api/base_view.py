# coding=utf-8
from django.http import HttpResponse
from django.views.generic import View


class HttpApiBaseView(View):

    def get(self, request, *args, **kwargs):
        data = self.get_data(request, *args, **kwargs)
        return HttpResponse(data)

    def post(self, request, *args, **kwargs):
        data = self.post_data(request)
        return HttpResponse(data)

    def post_data(self, request):
        return self._post_data(request)

    def _post_data(self, request):
        raise NotImplementedError

    def get_data(self, request, *args, **kwargs):
        return self._get_data(request)

    def _get_data(self, request):
        raise NotImplementedError

