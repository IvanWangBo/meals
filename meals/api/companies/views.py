#coding=utf-8
import random
import json

from api.base_view import HttpApiBaseView
from api.users.models import Users
from api.companies.models import Departments
from api.companies.models import Companies
from api.companies.models import RestaurantRelation
from api.restaurants.models import Dishes
from api.restaurants.models import Restaurants
from api.restaurants.models import TimeRange
from api.users.models import MealOrders
from api.decorators import admin_required
from api.decorators import company_required
from api.decorators import login_required
from common.constants import OrderStatus
from common.constants import UserAdminType
from api.companies.serializers import AddCompanySerializer
from api.companies.serializers import AddCompanyAdminSerializer
from api.companies.serializers import ResetCompanyAdminSerializer
from api.companies.serializers import AddDepartmentSerializer
from api.companies.serializers import RestaurantOrdersSummarySerializer
from api.companies.serializers import RestaurantOrdersDetailsSerializer
from api.companies.serializers import OrderSummarySerializer
from api.companies.serializers import OrderDetailsSerializer
from api.companies.serializers import AcceptOrdersSerializer
from api.companies.serializers import ModifyCompanyImageSerializer
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
            admin_name = 'BJ%03d' % company.id
            password = random.randint(10000000, 99999999)
            phone_number = data["phone_number"]
            company_admin = cacher.create_user(admin_name, password, admin_type=UserAdminType.company, company_id=company.id, phone_number=phone_number, real_name=u"管理员")
            company.save()
            return self.success_response({"company_id": company.id, "admin_name": admin_name, "password": password}, message=u'公司创建成功，管理员账号: %s, 初始密码: %s， 请牢记初始密码，或可在账号管理重置管理员密码。' % (admin_name, password))
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
            user_id = data['user_id']
            user = Users.objects.get(id=user_id)
            if not user:
                return self.error_response({}, u'该管理员不存在')
            user.set_password(data["password"])
            user.save()
            return self.success_response({'password': data["password"]}, u"密码设置成功")
        except Exception as err:
            return self.error_response({}, u"密码重置失败")


class DepartmentListView(HttpApiBaseView):
    @company_required
    def get(self, request):
        try:
            company_id = self.get_login_user_company_id(request)
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
            company_id = self.get_login_user_company_id(request)
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
            serializer = RestaurantOrdersSummarySerializer(data=request.GET)
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


class OrderSummaryOfCompanyView(HttpApiBaseView):
    @admin_required
    def get(self, request):
        try:
            serializer = OrderSummarySerializer(data=request.GET)
            if not serializer.is_valid():
                return self.serializer_invalid_response(serializer)
            data = serializer.data
            month = data["month"]
            year = data["year"]
            all_order_list = MealOrders.objects.filter(status=OrderStatus.accepted)
            order_list = []
            for order in all_order_list:
                if order.create_time.year == year and order.create_time.month == month:
                    order_list.append(order)
            company_id_rmb_map = {}
            order_info_list = []
            for order in order_list:
                company_id = Users.objects.get(id=order.user_id).company_id
                order_info_list.append({
                    'order_id': order.order_id,
                    'dish_id': order.dish_id,
                    'user_id': order.user_id,
                    'company_id': company_id,
                    'restaurant_id': Dishes.objects.get(id=order.dish_id).restaurant_id,
                    'total_price': order.total_price,
                    'create_time': order.create_time
                })
                company_id_rmb_map[company_id] = 0

            for order_info in order_info_list:
                company_id_rmb_map[order_info['company_id']] += order_info['total_price']
            result = []
            company_list = Companies.objects.all()
            for company in company_list:
                if company.id not in company_id_rmb_map:
                    result.append({
                        'company_id': company.id,
                        'company_name': company.company_name,
                        'total_rmb': 0
                    })
            for company_id in company_id_rmb_map:
                try:
                    company_name = Companies.objects.get(id=company_id).company_name
                except:
                    continue
                result.append({
                    'company_id': company_id,
                    'company_name': company_name,
                    'total_rmb': company_id_rmb_map[company_id]
                })
            return self.success_response(result, message=u"订单查询成功")
        except Exception as err:
            return self.error_response({}, u"订单查询失败")


class OrderListOfCompanyView(HttpApiBaseView):
    @admin_required
    def get(self, request):
        try:
            serializer = OrderDetailsSerializer(data=request.GET)
            if not serializer.is_valid():
                return self.serializer_invalid_response(serializer)
            data = serializer.data
            month = data["month"]
            year = data["year"]
            day = data["day"]
            company_id = data["company_id"]
            users = Users.objects.filter(company_id=company_id)
            user_id_list = [user.id for user in users]
            user_id_name_map = {}
            for user in users:
                user_id_name_map[user.id] = user.real_name
            all_orders = MealOrders.objects.filter(user_id__in=user_id_list, status__in=[OrderStatus.accepted, OrderStatus.created])
            orders = []
            for order in all_orders:
                if order.create_time.month == month and order.create_time.year == year and order.create_time.day == day:
                    orders.append(order)

            result = []
            total_rmb = 0
            for order in orders:
                dish = Dishes.objects.get(id=order.dish_id)
                restaurant = Restaurants.objects.get(id=dish.restaurant_id)
                time_range = TimeRange.objects.get(id=order.time_range)
                result.append({
                    "order_id": order.order_id,
                    "user_id": order.user_id,
                    "user_real_name": user_id_name_map.get(order.user_id, ""),
                    "status_name": OrderStatus.map.get(order.status, ""),
                    "status": order.status,
                    "dish_id": order.dish_id,
                    "dish_name": dish.name,
                    "dish_count": order.count,
                    "total_price": order.total_price,
                    "restaurant_id": dish.restaurant_id,
                    "restaurant_name": restaurant.name,
                    "time_range": order.time_range,
                    "time_range_name": time_range.name
                })
                total_rmb += order.total_price
            return self.success_response({"total_rmb": total_rmb, "order_list": result}, message=u"订单查询成功")
        except Exception as err:
            return self.error_response({}, message=u"订单查询失败")


class AcceptOrdersView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        try:
            serializer = AcceptOrdersSerializer(data=request.data)
            if not serializer.is_valid():
                return self.serializer_invalid_response(serializer)
            data = serializer.data
            try:
                order_id_list = json.loads(data["order_id_list"])
            except Exception as err:
                return self.error_response({}, u"order_id_list 格式错误")
            orders = MealOrders.objects.filter(order_id__in=order_id_list, status=OrderStatus.created)
            for order in orders:
                order.status = OrderStatus.accepted
                order.save()
            return self.success_response({}, u"接单成功")
        except Exception as err:
            return self.error_response({}, u"接单失败, error: %s" % err)

class ModifyCompanyImageView(HttpApiBaseView):
    @company_required
    def post(self, request):
        try:
            serializer = ModifyCompanyImageSerializer(data=request.data)
            company_id = self.get_login_user_company_id(request)
            if not serializer.is_valid():
                return self.serializer_invalid_response(serializer)
            data = serializer.data
            image_url = data['image_url']
            try:
                company = Companies.objects.get(id=company_id)
            except Exception as err:
                return self.error_response({}, u"您所在的公司不存在！")
            company.image_url = image_url
            company.save()
            return self.success_response({}, u"修改公司图片成功！")
        except Exception as err:
            return self.error_response({}, u"修改公司图片失败！")


class CompanyInfoView(HttpApiBaseView):
    @login_required
    def get(self, request):
        company_id = self.get_login_user_company_id(request)
        result = {'image_url': '', 'company_name': ''}
        try:
            company = Companies.objects.get(id=company_id)
        except Exception as err:
            return self.success_response(result, message=u"公司不存在")
        result['company_name'] = company.company_name
        result['image_url'] = company.image_url
        return self.success_response(result)
