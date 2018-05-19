# coding=utf8
from rest_framework.views import Response


class BaseException(RuntimeError):
    pass


class RequestBaseException(BaseException):
    def __init__(self, err_code, msg):
        super(RequestBaseException, self).__init__()
        self.message = msg
        self.err_code = err_code

    def json_response(self):
        return Response(data={"code": self.err_code, "message": self.message})

