#coding=utf-8
from api.base_view import HttpApiBaseView
from django.contrib import auth
from api.users.serializers import LoginSerializer


class LoginView(HttpApiBaseView):
    def post(self, request):
        """
        用户登录json api接口
        ---
        request_serializer: UserLoginSerializer
        """
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return self.serializer_invalid_response(serializer)
        data = serializer.data
        user = auth.authenticate(username=data["user_name"], password=data["password"])
        # 用户名或密码错误的话 返回None
        print user
        if user:
            auth.login(request, user)
            return self.success_response(data={'admin_type': user.admin_type}, message=u"登录成功")
        else:
            return self.error_response(data={}, message=u"用户名或密码错误")


class LogoutView(HttpApiBaseView):
    def post(self, request):
        auth.logout(request)
        return self.success_response(data={}, message=u"登出成功")
