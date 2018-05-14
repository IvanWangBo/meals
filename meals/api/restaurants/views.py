#coding=utf-8
import json

from api.base_view import HttpApiBaseView
from api.decorators import admin_required
from api.decorators import login_required
from api.restaurants.models import Dishes
from api.restaurants.models import TimeRange
from api.restaurants.serializers import AddDishSerializer
from api.restaurants.serializers import AddTimeRangeSerializer
from api.restaurants.serializers import DishesListSerializer


class AddDishView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        try:
            serializers = AddDishSerializer(data=request.data)
            if not serializers.is_valid():
                return self.error_response(serializers)
            data = serializers.data
            support_times = data["support_times"]
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
                support_times = json.dumps(data["support_times"])
            )
            dish.save()
        except Exception as err:
            return self.error_response({}, message=u"新建菜品失败")
        else:
            return self.success_response({
                "name": data["name"],
                "price": data["price"],
                "restaurant_id": data["restaurant_id"],
                "image_url": data["image_url"],
                "support_times": data["support_times"]
            }, message=u"新建菜品成功")


class DishesListView(HttpApiBaseView):
    @login_required
    def get(self, request):
        serializers = DishesListSerializer(data=request.data)
        if not serializers.is_valid():
            return self.error_response(serializers)
        data = serializers.data
        restaurant_id = data["restaurant_id"]
        time_range_id = data["time_range_id"]
        all_dishes = Dishes.objects.filter(restaurant_id=restaurant_id)
        right_dishes = []
        for dish in all_dishes:
            support_times = json.loads(dish.support_times)
            if time_range_id in support_times:
                right_dishes.append({
                    "dish_id": dish.id,
                    "name": dish.name,
                    "price": dish.price,
                    "image_url": dish.image_url,
                })
        return self.success_response(right_dishes, message=u"查询菜单成功")


class TimeRangeListView(HttpApiBaseView):
    @login_required
    def get(self, request):
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


class AddTimeRangeView(HttpApiBaseView):
    @admin_required
    def post(self, request):
        try:
            serializers = AddTimeRangeSerializer(data=request.data)
            if not serializers.is_valid():
                return self.error_response(serializers)
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


class EnableDishTime(HttpApiBaseView):
    @admin_required
    def post(self, request):
        pass


class DisableDishTime(HttpApiBaseView):
    @admin_required
    def post(self, request):
        pass



