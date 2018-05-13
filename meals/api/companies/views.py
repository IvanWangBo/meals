#coding=utf-8
import random

from api.base_view import HttpApiBaseView
from api.users.models import Users
from api.companies.models import Companies
from api.decorators import admin_required
from common.constants import UserAdminType
from django.contrib import auth
from api.companies.serializers import AddCompanySerializer
from api.companies.serializers import AddCompanyAdminSerializer
from api.companies.serializers import ResetCompanyAdminSerializer
from api.instances import cacher


class CompanyAdminView(HttpApiBaseView):
    @admin_required
    def get(self, request):
        users = Users.objects.filter(admin_type=UserAdminType.admin)
        companies = Companies.objects.all()
        company_id_name_map = {}
        for company in companies:
            company_id_name_map[company.id] = company.company_name
        results = []
        for user in users:
            company_id = user.company_id
            user_name = user.user_name
            phone_number = user.phone_number
            company_name = company_id_name_map.get(company_id, '')
            results.append({
                'company_id': company_id,
                'user_id': user.id,
                'user_name': user_name,
                'phone_number': phone_number,
                'company_name': company_name
            })
        return self.success_response(results)


class AddCompanyView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        serializer = AddCompanySerializer(data=request.data)
        if not serializer.is_valid():
            raise self.serializer_invalid_response(serializer)
        data = serializer.data
        try:
            company = Companies.objects.create(company_name=data["company_name"], province=data["province"], address=data["address"], is_enabled=1)
            admin_name = 'admin%03d' % company.id
            password = random.randint(10000000, 99999999)
            phone_number = serializer.phone_number
            company_admin = cacher.create_user(admin_name, password, admin_type=UserAdminType.company, company_id=company.id, phone_number=phone_number)
            company.save()
        except Exception as err:
            return self.error_response({}, message=u'公司创建失败')
        else:
            return self.success_response({'company_id': company.id, 'admin_name': admin_name, 'password': password}, message=u'公司创建成功')


class AddCompanyAdminView(HttpApiBaseView):
    @admin_required
    def get(self, request):
        companies = Companies.objects.all()
        results = []
        for company in companies:
            results.append({
                'company_id': company.id,
                'company_name': company.company_name
            })
        return self.success_response(results)

    @admin_required
    def post(self, request):
        serializer = AddCompanyAdminSerializer(data=request.data)
        if not serializer.is_valid():
            raise self.serializer_invalid_response(serializer)
        data = serializer.data
        company = Companies.objects.get(id=data["company_id"])
        if not company:
            return self.error_response({}, message=u"没有ID为: %s 的公司" % data["company_id"])
        try:
            company_admin = cacher.create_user(data["admin_name"], data["password"], admin_type=UserAdminType.company, company_id=company.id)
        except Exception as err:
            return self.error_response({}, message=u'公司管理员创建失败')
        else:
            return self.success_response({'company_id': company.id, 'admin_name': company_admin.user_name, 'password': data["password"]}, u"公司管理员创建成功")


class ResetCompanyAdminView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        serializer = ResetCompanyAdminSerializer(data=request.data)
        if not serializer.is_valid():
            raise self.serializer_invalid_response(serializer)
        data = serializer.data
        user = Users.objects.get(id=data["user_id"])
        if not user:
            return self.error_response({}, u'该管理员不存在')
        user.set_password(data["password"])
        return self.success_response({'password': data["password"]}, u"密码设置成功")
