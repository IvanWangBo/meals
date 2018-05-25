#coding=utf-8
import random

from api.base_view import HttpApiBaseView
from api.users.models import Users
from api.companies.models import Departments
from api.companies.models import Companies
from api.companies.models import RestaurantRelation
from api.restaurants.models import Dishes
from api.restaurants.models import Restaurants
from api.users.models import MealOrders
from api.decorators import admin_required
from api.decorators import company_required
from common.constants import OrderStatus
from common.constants import UserAdminType
from api.companies.serializers import AddCompanySerializer
from api.companies.serializers import AddCompanyAdminSerializer
from api.companies.serializers import ResetCompanyAdminSerializer
from api.companies.serializers import AddDepartmentSerializer
from api.companies.serializers import RestaurantOrdersSummarySerializer
from api.companies.serializers import RestaurantOrdersDetailsSerializer
from api.instances import cacher


class CompanyAdminView(HttpApiBaseView):
    @admin_required
    def get(self, request):
        users = Users.objects.filter(admin_type=UserAdminType.company)
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
                "company_id": company_id,
                "user_id": user.id,
                "user_name": user_name,
                "phone_number": phone_number,
                "company_name": company_name
            })
        return self.success_response(results)


class AddCompanyView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        try:
            serializer = AddCompanySerializer(data=request.data)
            if not serializer.is_valid():
                return self.serializer_invalid_response(serializer)
            data = serializer.data
            company = Companies.objects.create(company_name=data["company_name"], province=data["province"], address=data["address"], is_enabled=1)
            admin_name = 'admin%03d' % company.id
            password = random.randint(10000000, 99999999)
            phone_number = data["phone_number"]
            company_admin = cacher.create_user(admin_name, password, admin_type=UserAdminType.company, company_id=company.id, phone_number=phone_number)
            company.save()
            return self.success_response({"company_id": company.id, "admin_name": admin_name, "password": password}, message=u'公司创建成功')
        except Exception as err:
            return self.error_response({}, message=u'公司创建失败')


class CompanyListView(HttpApiBaseView):
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


class AddCompanyAdminView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        try:
            serializer = AddCompanyAdminSerializer(data=request.data)
            if not serializer.is_valid():
                return self.serializer_invalid_response(serializer)
            data = serializer.data
            company = Companies.objects.get(id=data["company_id"])
            if not company:
                return self.error_response({}, message=u"没有ID为: %s 的公司" % data["company_id"])
            company_admin = cacher.create_user(data["admin_name"], data["password"], admin_type=UserAdminType.company, company_id=company.id)
            return self.success_response({'company_id': company.id, 'admin_name': company_admin.user_name, 'password': data["password"]}, u"公司管理员创建成功")
        except Exception as err:
            return self.error_response({}, message=u'公司管理员创建失败')


class ResetCompanyAdminView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        try:
            serializer = ResetCompanyAdminSerializer(data=request.data)
            if not serializer.is_valid():
                return self.serializer_invalid_response(serializer)
            data = serializer.data
            user_id = self.get_login_user_id(request)
            user = Users.objects.get(id=user_id)
            if not user:
                return self.error_response({}, u'该管理员不存在')
            user.set_password(data["password"])
            return self.success_response({'password': data["password"]}, u"密码设置成功")
        except Exception as err:
            return self.error_response({}, u"密码重置失败")


class DepartmentListView(HttpApiBaseView):
    @company_required
    def get(self, request):
        try:
            company_id = request.GET.get("company_id")
            user_id = self.get_login_user_id(request)
            self.check_user_company(user_id, company_id)
            if company_id is None:
                return self.error_response(data={}, message=u"该公司不存在")
            departments = Departments.objects.filter(company_id=company_id)
            results = [{"department_id": department.id, "department_name": department.name} for department in departments]
            return self.success_response(results, message=u"获取部门列表成功")
        except Exception as err:
            return self.error_response({}, message=u"获取部门列表失败")


class AddDepartmentView(HttpApiBaseView):
    @company_required
    def post(self, request):
        try:
            serializer = AddDepartmentSerializer(data=request.data)
            if not serializer.is_valid():
                return self.serializer_invalid_response(serializer)
            data = serializer.data
            company_id = data["company_id"]
            name = data["department_name"]
            user_id = self.get_login_user_id(request)
            self.check_user_company(user_id, company_id)
            department = Departments.objects.create(name=name, company_id=company_id)
            department.save()
            return self.success_response({
                'department_id': department.id,
                'department_name': department.name,
                'company_id': department.company_id
            }, u"创建部门成功")
        except Exception as err:
            return self.error_response({}, u"创建部门失败")


class RestaurantOrdersSummaryView(HttpApiBaseView):
    @company_required
    def get(self, request):
        try:
            serializer = RestaurantOrdersSummarySerializer(data=request.data)
            if not serializer.is_valid():
                return self.serializer_invalid_response(serializer)
            data = serializer.data
            company_id = self.get_login_user_company_id(request)
            month = data["month"]
            year = data["year"]
            users = Users.objects.filter(company_id=company_id)
            user_id_list = [user.id for user in users]
            all_order_list = MealOrders.objects.filter(user_id__in=user_id_list, status=OrderStatus.accepted)
            order_list = []
            for order in all_order_list:
                if order.create_time.year == year and order.create_time.month == month:
                    order_list.append(order)
            restaurant_id_rmb_map = {}
            order_info_list = []
            for order in order_list:
                order_info_list.append({
                    'order_id': order.order_id,
                    'dish_id': order.dish_id,
                    'restaurant_id': Dishes.objects.get(id=order.dish_id).restaurant_id,
                    'total_price': order.total_price,
                    'create_time': order.create_time
                })
                restaurant_id_rmb_map[Dishes.objects.get(id=order.dish_id).restaurant_id] = 0

            for order_info in order_info_list:
                restaurant_id_rmb_map[order_info['restaurant_id']] += order_info['total_price']
            result = []
            for restaurant_id in restaurant_id_rmb_map:
                result.append({
                    'restaurant_id': restaurant_id,
                    'restaurant_name': Restaurants.objects.get(id=restaurant_id).name,
                    'total_rmb': restaurant_id_rmb_map[restaurant_id]
                })
            return self.success_response(result, message=u"订单查询成功")
        except Exception as err:
            return self.error_response({}, u"订单查询失败")


class RestaurantOrdersDetailsView(HttpApiBaseView):
    @company_required
    def get(self, request):
        try:
            serializer = RestaurantOrdersDetailsSerializer(data=request.GET)
            if not serializer.is_valid():
                return self.serializer_invalid_response(serializer)
            data = serializer.data
            company_id = self.get_login_user_company_id(request)
            year = data["year"]
            month = data["month"]
            restaurant_id = data["restaurant_id"]
            support_dishes = Dishes.objects.filter(restaurant_id=restaurant_id)
            dish_id_list = [dish.id for dish in support_dishes]
            users = Users.objects.filter(company_id=company_id)
            user_id_list = [user.id for user in users]

            all_order_list = MealOrders.objects.filter(user_id__in=user_id_list, dish_id__in=dish_id_list, status=OrderStatus.accepted)
            order_list = []
            for order in all_order_list:
                if order.create_time.year == year and order.create_time.month == month:
                    order_list.append(order)

            result_map = {}

            for order in order_list:
                result_map[order.create_time.date()] = {}
            for key in result_map:
                for dish_id in dish_id_list:
                    result_map[key][dish_id] = {
                        'count': 0,
                        'total_price': 0
                    }
            for order in order_list:
                result_map[order.create_time.date()][order.dish_id]['count'] += order.count
                result_map[order.create_time.date()][order.dish_id]['total_price'] += order.total_price

            orders = []
            total_rmb = 0
            for create_date in result_map:
                daily_map = result_map[create_date]
                for dish_id in daily_map:
                    if daily_map[dish_id]['count']:
                        orders.append({
                            'create_date': create_date,
                            'dish_id': dish_id,
                            'count': daily_map[dish_id]['count'],
                            'total_price': daily_map[dish_id]['total_price'],
                            'dish_name': Dishes.objects.get(id=dish_id).name,
                        })
                        total_rmb += daily_map[dish_id]['total_price']
            result = {
                'order_list': orders,
                'total_rmb': total_rmb
            }
            return self.success_response(result, message=u"订单查询成功")
        except Exception as err:
            return self.error_response({}, u"订单查询失败")

    def _get_order_price(self, order_list):
        order_price = 0
        for order in order_list:
            order_price += order['total_price']
        return order_price
