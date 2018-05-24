#coding=utf-8
import json

from api.base_view import HttpApiBaseView
from api.decorators import admin_required
from api.decorators import login_required
from api.decorators import company_required
from api.restaurants.models import Dishes
from api.restaurants.models import TimeRange
from api.restaurants.models import Restaurants
from api.companies.models import RestaurantRelation
from api.restaurants.serializers import DeleteRestaurantSerializer
from api.restaurants.serializers import AddDishSerializer
from api.restaurants.serializers import AddTimeRangeSerializer
from api.restaurants.serializers import ModifyTimeRangeSerializer
from api.restaurants.serializers import DeleteDishSerializer
from api.restaurants.serializers import DishesListSerializer
from api.restaurants.serializers import AddRestaurantSerializer
from api.restaurants.serializers import ModifyDishSerializer
from api.restaurants.serializers import RestaurantRelationSerializer


class AddDishView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        try:
            serializers = AddDishSerializer(data=request.data)
            if not serializers.is_valid():
                return self.serializer_invalid_response(serializers)
            data = serializers.data
            support_times = json.loads(data["support_times"])
            for support_time in support_times:
                try:
                    time_range = TimeRange.objects.get(id=support_time)
                except Exception as err:
                    return self.error_response({}, u"所选时间段无效")
                else:
                    if not time_range:
                        return self.error_response({}, u"所选时间段无效")
            dish = Dishes.objects.create(
                name=data["name"],
                price=data["price"],
                restaurant_id=data["restaurant_id"],
                image_url=data["image_url"],
                support_times = data["support_times"]
            )
            dish.save()
        except Exception as err:
            return self.error_response({}, message=u"新建菜品失败")
        else:
            return self.success_response({
                "dish_id": dish.id,
                "name": data["name"],
                "price": data["price"],
                "restaurant_id": data["restaurant_id"],
                "image_url": data["image_url"],
                "support_times": data["support_times"]
            }, message=u"新建菜品成功")


class RestaurantRelationView(HttpApiBaseView):
    @company_required
    def get(self, request):
        try:
            company_id = self.get_login_user_company_id(request)
            serializers = RestaurantRelationSerializer(data=request.GET)
            data = serializers.data
            restaurant_id = data["restaurant_id"]
            try:
                is_enabled = RestaurantRelation.objects.get(restaurant_id=restaurant_id, company_id=company_id).is_enabled
            except Exception as err:
                is_enabled = 0
            return self.success_response({'is_enabled': is_enabled}, message=u"查询成功")
        except Exception as err:
            return self.error_response({}, message=u"查询失败")

    @company_required
    def post(self, request):
        try:
            company_id = self.get_login_user_company_id(request)
            serializers = RestaurantRelationSerializer(data=request.GET)
            data = serializers.data
            restaurant_id = data["restaurant_id"]
            is_enabled = data["is_enabled"]
            try:
                relation = RestaurantRelation.objects.get(restaurant_id=restaurant_id, company_id=company_id)
                relation.is_enabled = is_enabled
                relation.save()
            except:
                relation = RestaurantRelation.objects.create(restaurant_id=restaurant_id, company_id=company_id, is_enabled=is_enabled)
                relation.save()
            return self.success_response({}, u"修改成功")
        except Exception as err:
            return self.error_response({}, u"修改失败")


class DishesListView(HttpApiBaseView):
    @login_required
    def get(self, request):
        try:
            serializers = DishesListSerializer(data=request.GET)
            if not serializers.is_valid():
                return self.serializer_invalid_response(serializers)
            data = serializers.data
            restaurant_id = data["restaurant_id"]
            time_range_id = data["time_range_id"]
            all_dishes = Dishes.objects.filter(restaurant_id=restaurant_id, is_enabled=1)
            right_dishes = []
            if time_range_id == -9:
                right_dishes = all_dishes
            else:
                for dish in all_dishes:
                    support_times = json.loads(dish.support_times)
                    support_times_name = []
                    for support_time in support_times:
                        support_times_name.append(TimeRange.objects.get(id=support_time).name[1])
                    if time_range_id in support_times:
                        right_dishes.append({
                            "dish_id": dish.id,
                            "name": dish.name,
                            "price": dish.price,
                            "image_url": dish.image_url,
                            "support_times": support_times,
                            "support_times_name": support_times_name,
                        })
            return self.success_response(right_dishes, message=u"查询菜单成功")
        except Exception as err:
            return self.error_response({}, message=u"查询菜单失败")


class TimeRangeListView(HttpApiBaseView):
    @login_required
    def get(self, request):
        try:
            result = []
            time_range_list = TimeRange.objects.all()
            for time_range in time_range_list:
                result.append({
                    'time_range_id': time_range.id,
                    'name': time_range.name,
                    'start_time': time_range.start_time,
                    'end_time': time_range.end_time
                })
            return self.success_response(result, message=u"获取用餐时段成功")
        except Exception as err:
            return self.error_response({}, message=u"获取用餐时段失败")


class AddTimeRangeView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        try:
            serializers = AddTimeRangeSerializer(data=request.data)
            if not serializers.is_valid():
                return self.serializer_invalid_response(serializers)
            data = serializers.data
            name = data['name']
            start_time = data['start_time']
            end_time = data['end_time']
            time_range = TimeRange.objects.create(name=name, start_time=start_time, end_time=end_time)
            time_range.save()
        except Exception as err:
            return self.error_response({}, message=u"新建用餐时段失败")
        else:
            return self.success_response({'time_range_id': time_range.id, 'start_time': start_time, 'end_time': end_time}, message=u"新建用餐时间段成功")


class EnableDishTimeView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        try:
            serializers = ModifyTimeRangeSerializer(data=request.data)
            if not serializers.is_valid():
                return self.serializer_invalid_response(serializers)
            data = serializers.data
            dish_id = data["dish_id"]
            time_range_id = data["time_range_id"]
            dish = Dishes.objects.get(id=dish_id)
            time_range = TimeRange.objects.get(id=time_range_id)
            support_times = json.loads(dish.support_times)
            if time_range_id not in support_times:
                support_times.append(time_range_id)
                dish.support_times = json.dumps(support_times)
                dish.save()
        except Exception as err:
            return self.error_response({}, message=u"应用用餐时段失败")
        else:
            return self.success_response({
                "dish_id": dish.id,
                "name": dish.name,
                "price": dish.price,
                "image_url": dish.image_url,
                "support_times": support_times
            }, message=u"应用用餐时段成功")


class ModifyDishView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        try:
            serializers = ModifyDishSerializer(data=request.data)
            if not serializers.is_valid():
                return self.serializer_invalid_response(serializers)
            data = serializers.data
            dish_id = data["dish_id"]
            dish = Dishes.objects.get(id=dish_id)
            dish_name = data.get("name")
            if dish_name:
                dish.name = dish_name
            dish_price = data.get("price")
            if dish_price:
                dish.price = dish_price
            support_times_str = data["support_times"]
            image_url = data.get("image_url")
            if image_url:
                dish.image_url = image_url
            if support_times_str:
                try:
                    support_times_str = json.loads(support_times_str)
                except:
                    return self.error_response({}, u"support_times 格式错误")
                dish.support_times = support_times_str
            dish.save()
            return self.success_response({
                "dish_id": dish.id,
                "name": dish.name,
                "price": dish.price,
                "image_url": dish.image_url,
                "support_times": json.dumps(dish.support_times)
            }, u"修改菜品信息成功!")

        except Exception as err:
            return self.error_response({}, u"修改菜品信息失败")


class DisableDishTimeView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        try:
            serializers = ModifyTimeRangeSerializer(data=request.data)
            if not serializers.is_valid():
                return self.serializer_invalid_response(serializers)
            data = serializers.data
            dish_id = data["dish_id"]
            time_range_id = data["time_range_id"]
            dish = Dishes.objects.get(id=dish_id)
            time_range = TimeRange.objects.get(id=time_range_id)
            support_times = json.loads(dish.support_times)
            if time_range_id in support_times:
                support_times.remove(time_range_id)
                dish.support_times = json.dumps(support_times)
                dish.save()
        except Exception as err:
            return self.error_response({}, message=u"取消用餐时段失败")
        else:
            return self.success_response({
                "dish_id": dish.id,
                "name": dish.name,
                "price": dish.price,
                "image_url": dish.image_url,
                "support_times": support_times
            }, message=u"取消用餐时段成功")


class AddRestaurantView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        try:
            serializers = AddRestaurantSerializer(data=request.data)
            if not serializers.is_valid():
                return self.serializer_invalid_response(serializers)
            data = serializers.data
            name = data['restaurant_name']
            phone_number = data['phone_number']
            address = data['address']
            restaurant = Restaurants.objects.create(name=name, address=address, phone_number=phone_number, is_enabled=1)
            restaurant.save()
        except Exception as err:
            return self.error_response({}, u"创建餐厅失败")
        else:
            return self.success_response({
                "restaurant_id": restaurant.id,
                "restaurant_name": name,
                "address": address,
                "phone_number": phone_number
            }, u"创建餐厅成功")


class RestaurantListView(HttpApiBaseView):
    @login_required
    def get(self, request):
        try:
            is_order = request.GET.get('is_order', 0)
            all_restaurants = Restaurants.objects.filter(is_enabled=1)
            if is_order:
                company_id = self.get_login_user_company_id(request)
                relations = RestaurantRelation.objects.filter(company_id=company_id, is_enabled=1)
                restaurant_ids = [relation.restaurant_id for relation in relations]
                restaurants = []
                for restaurant in all_restaurants:
                    if restaurant.id in restaurant_ids:
                        restaurants.append(restaurant)
            else:
                restaurants = all_restaurants
            results = [{
                'restaurant_id': restaurant.id,
                'restaurant_name': restaurant.name,
                'address': restaurant.address,
                'phone_number': restaurant.phone_number
            } for restaurant in restaurants]
            return self.success_response(results, message=u"获取餐厅列表成功")

        except Exception as err:
            return self.error_response({}, u"获取餐厅列表失败")


class DeleteRestaurantView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        try:
            serializers = DeleteRestaurantSerializer(data=request.data)
            if not serializers.is_valid():
                return self.serializer_invalid_response(serializers)
            data = serializers.data
            restaurant_id = data["restaurant_id"]
            restaurant = Restaurants.objects.get(id=restaurant_id)
            restaurant.is_enabled = 0
            restaurant.save()
            return self.success_response({}, message=u"删除餐厅成功")
        except Exception as err:
            return self.error_response({}, message=u"删除餐厅失败")


class DeleteDishView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        try:
            serializers = DeleteDishSerializer(data=request.data)
            if not serializers.is_valid():
                return self.serializer_invalid_response(serializers)
            data = serializers.data
            dish_id = data["dish_id"]
            dish = Dishes.objects.get(id=dish_id)
            dish.is_enabled = 0
            dish.save()
            return self.success_response({}, message=u"删除菜品成功")
        except Exception as err:
            return self.error_response({}, message=u"删除菜品失败")
