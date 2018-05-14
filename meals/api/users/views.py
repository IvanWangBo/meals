#coding=utf-8
from api.base_view import HttpApiBaseView
from django.contrib import auth
from api.users.serializers import LoginSerializer
from api.users.serializers import AddPersonnelSerializer
from api.companies.models import Departments
from api.instances import cacher
from api.users.models import Users
from api.users.serializers import ResetUserSerializer
from common.constants import UserAdminType
from api.decorators import login_required
from api.decorators import company_required


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
            return self.success_response(data={
                'admin_type': user.admin_type,
                'user_id': user.id,
                'company_id': user.company_id
            }, message=u"登录成功")
        else:
            return self.error_response(data={}, message=u"用户名或密码错误")


class PersonnelListView(HttpApiBaseView):
    def get(self, request):
        try:
            company_id = request.GET.get("company_id")
            if company_id is None:
                return self.error_response(data={}, message=u"该公司不存在")
            personnel_list = Users.objects.filter(company_id=company_id)
            departments = Departments.objects.filter(company_id=company_id)
            department_map = {}
            for department in departments:
                department_map[department.id] = department.name
            results = []
            for user in personnel_list:
                results.append({
                    'user_id': user.id,
                    'department_id': user.department_id,
                    'department_name': department_map.get(user.department_id, ''),
                    'name': user.real_name,
                    'left_rmb': 0,
                    'to_settle': 0
                })
        except Exception as err:
            return self.error_response({}, u"获取员工列表失败")
        else:
            return self.success_response(results, message=u"获取员工列表成功")


class AddPersonnelView(HttpApiBaseView):
    @company_required
    def get(self, request):
        company_id = request.GET.get("company_id")
        if company_id is None:
            return self.error_response(data={}, message=u"该公司不存在")
        departments = Departments.objects.filter(company_id=company_id)
        results = [{"department_id": department.id, "department_name": department.name} for department in departments]
        return self.success_response(results)

    @company_required
    def post(self, request):
        try:
            serializer = AddPersonnelSerializer(data=request.data)
            if not serializer.is_valid():
                raise self.serializer_invalid_response(serializer)
            data = serializer.data
            user = cacher.create_user(
                user_name=data["user_name"],
                real_name=data["real_name"],
                company_id=data["company_id"],
                department_id=data["department_id"],
                gender=data["gender"],
                phone_number=data["phone_number"],
                admin_type=UserAdminType.personnel
            )
            user.set_password(data["password"])
        except Exception as err:
            return self.error_response({}, message=u"新建员工账号失败!")
        else:
            return self.success_response({}, message=u"新建员工账号成功!")


class ResetUserView(HttpApiBaseView):
    @login_required
    def post(self, request):
        serializer = ResetUserSerializer(data=request.data)
        if not serializer.is_valid():
            raise self.serializer_invalid_response(serializer)
        data = serializer.data
        user = Users.objects.get(id=data["user_id"])
        if not user:
            return self.error_response({}, message=u"该用户不存在")
        if not user.check_password(data["password"]):
            return self.error_response({}, message=u"原密码输入错误!")
        user.set_password(data["new_password"])
        return self.success_response({}, message=u"用户密码修改成功")


class LogoutView(HttpApiBaseView):
    @login_required
    def post(self, request):
        auth.logout(request)
