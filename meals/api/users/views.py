#coding=utf-8
import json

from api.base_view import HttpApiBaseView
from django.contrib import auth
from api.users.serializers import LoginSerializer
from api.users.serializers import AddPersonnelSerializer
from api.companies.models import Departments
from api.users.models import MealOrders
from api.restaurants.models import Dishes
from api.instances import cacher
from api.users.models import Users
from api.users.serializers import ResetUserSerializer
from api.users.serializers import MealsOrderSerializer
from api.users.serializers import CancelMealsOrderSerializer
from api.users.serializers import MealsOrderListSerializer
from common.constants import UserAdminType
from common.constants import OrderStatus
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
    @company_required
    def get(self, request):
        try:
            company_id = request.GET.get("company_id")
            if company_id is None:
                return self.error_response(data={}, message=u"该公司不存在")
            user_id = self.get_login_user_id(request)
            self.check_user_company(user_id, company_id)
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
                    'real_name': user.real_name,
                    'left_rmb': 0,
                    'to_settle': 0
                })
            return self.success_response(results, message=u"获取员工列表成功")
        except Exception as err:
            return self.error_response({}, u"获取员工列表失败")


class AddPersonnelView(HttpApiBaseView):
    @company_required
    def get(self, request):
        company_id = request.GET.get("company_id")
        if company_id is None:
            return self.error_response(data={}, message=u"该公司不存在")
        user_id = self.get_login_user_id(request)
        self.check_user_company(user_id, company_id)
        departments = Departments.objects.filter(company_id=company_id)
        results = [{"department_id": department.id, "department_name": department.name} for department in departments]
        return self.success_response(results)

    @company_required
    def post(self, request):
        try:
            serializer = AddPersonnelSerializer(data=request.data)
            if not serializer.is_valid():
                return self.serializer_invalid_response(serializer)
            data = serializer.data
            user_id = self.get_login_user_id(request)
            self.check_user_company(user_id, data["company_id"])
            user = cacher.create_user(
                user_name=data["user_name"],
                password=data["password"],
                real_name=data["real_name"],
                company_id=data["company_id"],
                department_id=data["department_id"],
                gender=data["gender"],
                phone_number=data["phone_number"],
                admin_type=UserAdminType.personnel
            )
            return self.success_response({
                "user_id": user.id,
                "user_name": user.user_name,
                "real_name": user.real_name,
                "company_id": user.company_id,
                "department_id": user.department_id,
                "gender": user.gender,
                "phone_number": user.phone_number,
                "admin_type": user.admin_type,
                "password": user.password
            }, message=u"新建员工账号成功!")
        except Exception as err:
            return self.error_response({}, message=u"新建员工账号失败!")


class ResetUserView(HttpApiBaseView):
    @login_required
    def post(self, request):
        try:
            serializer = ResetUserSerializer(data=request.data)
            if not serializer.is_valid():
                return self.serializer_invalid_response(serializer)
            data = serializer.data
            user_id = self.get_login_user_id(request)
            user = Users.objects.get(id=user_id)
            if not user:
                return self.error_response({}, message=u"该用户不存在")
            if not user.check_password(data["password"]):
                return self.error_response({}, message=u"原密码输入错误!")
            user.set_password(data["new_password"])
            return self.success_response({}, message=u"用户密码修改成功")
        except Exception as err:
            return self.error_response({}, message=u"用户修改密码失败")


class LogoutView(HttpApiBaseView):
    @login_required
    def post(self, request):
        auth.logout(request)
        return self.success_response({}, message=u"登出成功")


class MealsOrderView(HttpApiBaseView):
    @login_required
    def post(self, request):
        try:
            serializer = MealsOrderSerializer(data=request.data)
            if not serializer.is_valid():
                return self.serializer_invalid_response(serializer)
            data = serializer.data
            user_id = self.get_login_user_id(request)
            order_list = json.loads(data['order_list'])
            order_id = cacher.get_order_id()
            order_total_price = 0
            for order in order_list:
                dish_id = order['dish_id']
                count = order['count']
                dish = Dishes.objects.get(id=dish_id)
                price = dish.price
                total_price = price * count
                order_total_price = order_total_price + total_price
                order = MealOrders.objects.create(
                    user_id=user_id,
                    order_id=order_id,
                    dish_id=dish_id,
                    count=count,
                    status=OrderStatus.created,
                    total_price=total_price,
                )
                order.save()
            return self.success_response({
                'user_id': user_id,
                'order_id': order_id,
                'order_list': order_list,
                'order_total_price': order_total_price
            }, u"下单成功")
        except Exception as err:
            return self.error_response({}, message=u"订餐失败, err: %s" % err)


class CancelMealsOrder(HttpApiBaseView):
    @login_required
    def post(self, request):
        try:
            serializer = CancelMealsOrderSerializer(data=request.data)
            if not serializer.is_valid():
                return self.serializer_invalid_response(serializer)
            data = serializer.data
            user_id = self.get_login_user_id(request)
            order_id = data["order_id"]
            order_list = MealOrders.objects.filter(order_id=order_id)
            can_cancel = all([order.state in (OrderStatus.created, OrderStatus.accepted) for order in order_list])
            if not can_cancel:
                return self.error_response({},message=u"订单派送中，无法取消")
            is_owner = all([order.user_id == user_id for order in order_list])
            if not is_owner:
                return self.error_response({},message=u"订单取消失败")
            for order in order_list:
                order.state = OrderStatus.canceled
                order.save()
            return self.success_response({}, message=u"订单取消成功！")
        except Exception as err:
            return self.error_response({}, message=u"取消订单失败, err: %s" % err)


class MealsOrderList(HttpApiBaseView):
    @login_required
    def get(self, request):
        try:
            serializer = MealsOrderListSerializer(data=request.data)
            if not serializer.is_valid():
                return self.serializer_invalid_response(serializer)
            data = serializer.data
            user_id = self.get_login_user_id(request)
            month = data["month"]
            all_orders = MealOrders.objects.filter(user_id=user_id)
            orders = []
            for order in all_orders:
                if order.create_time.month == month:
                    orders.append(order)
            result_map = {}
            extra_detail_map = {}
            for order in orders:
                result_map[order.order_id] = []
                extra_detail_map[order.order_id] = {}
            for order in orders:
                result_map[order.order_id].append({
                    'dish_id': order.dish_id,
                    'dish_name': Dishes.objects.get(id=order.dish_id).name,
                    'count': order.count,
                    'status': order.status,
                    'total_price': order.total_price,
                    'create_time': order.create_time
                })
                extra_detail_map[order.order_id]['create_time'] = order.create_time
                extra_detail_map[order.order_id]['status'] = order.status
            result = []
            for order_id in result_map:
                result.append({
                    'order_id': order_id,
                    'order_list': result_map[order_id],
                    'order_price': self._get_order_price(result_map[order_id]),
                    'create_time': extra_detail_map.get(order_id, {}).get('create_time', ''),
                    'status': extra_detail_map.get(order_id, {}).get('status', -2),
                })
            return self.success_response(result, message=u"订单查询成功！")
        except Exception as err:
            return self.error_response({}, message=u"")

    def _get_order_price(self, order_list):
        order_price = 0
        for order in order_list:
            order_price += order['total_price']
        return order_price
