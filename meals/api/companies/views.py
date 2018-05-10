#coding=utf-8
from api.base_view import HttpApiBaseView
from api.users.models import Users
from api.companies.models import Companies
from api.decorators import admin_required
from common.constants import UserAdminType
from django.contrib import auth
from api.companies.serializers import AddCompanySerializer
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
            company.save()
        except Exception as err:
            return self.error_response({}, message=u'公司创建失败')
        else:
            return self.success_response({}, message=u'公司创建成功')


class AddCompanyAdminView(HttpApiBaseView):
    @admin_required
    def get(self, request):
        return self.success_response({})

    @admin_required
    def post(self, request):
        return self.success_response({})
