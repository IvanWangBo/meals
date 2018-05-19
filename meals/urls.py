# coding=utf-8
import settings
from django.conf.urls import url
from django.contrib import admin
from api.users.views import LoginView
from api.users.views import LogoutView
from api.users.views import ResetUserView
from api.users.views import PersonnelListView
from api.users.views import MealsOrderView
from api.users.views import CancelMealsOrder
from api.users.views import MealsOrderList
from api.companies.views import CompanyAdminView
from api.companies.views import AddCompanyView
from api.companies.views import AddCompanyAdminView
from api.companies.views import ResetCompanyAdminView
from api.companies.views import AddDepartmentView
from api.companies.views import CompanyListView
from api.companies.views import DepartmentListView
from api.companies.views import RestaurantOrdersSummaryView
from api.companies.views import RestaurantOrdersDetailsView
from api.restaurants.views import AddDishView
from api.restaurants.views import DeleteDishView
from api.restaurants.views import TimeRangeListView
from api.restaurants.views import AddTimeRangeView
from api.restaurants.views import DishesListView
from api.restaurants.views import EnableDishTimeView
from api.restaurants.views import DisableDishTimeView
from api.restaurants.views import AddRestaurantView
from api.restaurants.views import RestaurantListView
from api.restaurants.views import DeleteRestaurantView
from api.restaurants.views import ModifyDishView
from api.users.views import AddPersonnelView
from django.views.generic import TemplateView
from api.opt.upload_image_view import UploadImageView


# 通用返回格式：
# 正确: {"code": 200, "data": data, "message": message}
# 错误: {"code": 401, "data": data, "message": message}

urlpatterns = [
    #url(r'^admin/', admin.site.urls),

    # html
    url(r"^$", TemplateView.as_view(template_name="login.html"), name="user_login_page"),
    url(r'^login/$', TemplateView.as_view(template_name="login.html"), name="user_login_page"),

    url(r'^personnel/index/$', TemplateView.as_view(template_name="personnel/index.html"), name="personnel_index_page"),

    url(r'^admin/index/$', TemplateView.as_view(template_name="admin/index.html"), name="admin_index_page"),
    url(r'^admin/restaurant/$', TemplateView.as_view(template_name="admin/restaurant.html"), name="admin_restaurant_page"),
    url(r'^admin/order/$', TemplateView.as_view(template_name="admin/order.html"), name="admin_order_page"),

    url(r'^company/index/$', TemplateView.as_view(template_name="company/index.html"), name="company_index_page"),
    url(r'^company/restaurant/$', TemplateView.as_view(template_name="company/restaurant.html"), name="company_restaurant_page"),
    url(r'^company/order/$', TemplateView.as_view(template_name="company/order.html"), name="company_order_page"),

    url(r'^restaurant/index/$', TemplateView.as_view(template_name="restaurant/index.html"), name="restaurant_index_page"),

    # user api
    url(r'^api/login/$', LoginView.as_view()), # 登录
    url(r'^api/logout/$', LogoutView.as_view()), # 登出
    url(r'^api/user/reset/', ResetUserView.as_view()), # 修改密码

    # 公司账号列表
    url(r'api/company/admin/$', CompanyAdminView.as_view()), # 公司账号列表
    # 添加公司及管理员
    url(r'^api/company/add/$', AddCompanyView.as_view()), # 添加公司及管理员
    # 公司列表
    url(r"api/company/list/$", CompanyListView.as_view()),
    # 添加公司管理员
    url(r'api/company/admin/add/$', AddCompanyAdminView.as_view()),
    # 重置管理员密码
    url(r'api/company/admin/reset/$', ResetCompanyAdminView.as_view()),

    # 创建部门
    url(r'api/company/department/add/$', AddDepartmentView.as_view()),

    # 部门列表 GET
    url(r'api/company/department/list/$', DepartmentListView.as_view()),

    # 所有商家商家总订单信息
    url(r"api/company/order/summary/$", RestaurantOrdersSummaryView.as_view()),

    # 商家日订单信息
    url(r"api/company/order/details/$", RestaurantOrdersDetailsView.as_view()),


    # 添加员工账号 POST
    url(r'api/user/add/$', AddPersonnelView.as_view()),
    # 获取员工列表
    url(r'api/user/list/$', PersonnelListView.as_view()),

    # 添加菜品
    url(r"api/restaurant/dish/add/$", AddDishView.as_view()),
    # 删除菜品
    url(r"api/restaurant/dish/delete/$", DeleteDishView.as_view()),
    # 菜品清单
    url(r"api/restaurant/dish/list/$", DishesListView.as_view()),
    # 修改菜品信息
    url(r"api/restaurant/dish/modify/$", ModifyDishView.as_view()),

    # 查询用餐时间段
    url(r"api/restaurant/time_range/list/$", TimeRangeListView.as_view()),
    # 新建用餐时间段
    url(r"api/restaurant/time_range/add/$", AddTimeRangeView.as_view()),
    # 启用用餐时间段
    url(r"api/restaurant/time_range/enable/$", EnableDishTimeView.as_view()),
    # 取消用餐时间段
    url(r"api/restaurant/time_range/disable/$", DisableDishTimeView.as_view()),

    # 创建餐厅
    url(r"api/restaurant/add/$", AddRestaurantView.as_view()),

    # 餐厅列表
    url(r"api/restaurant/list/$", RestaurantListView.as_view()),
    # 删除餐厅
    url(r"api/restaurant/delete/$", DeleteRestaurantView.as_view()),

    # 订餐
    url(r"api/user/meals/order/$", MealsOrderView.as_view()),
    # 取消订单
    url(r"api/user/meals/cancel/$", CancelMealsOrder.as_view()),
    # 查询订单
    url(r"api/user/meals/list/$", MealsOrderList.as_view()),

    # opt
    url(r"api/opt/upload_file/$", UploadImageView.as_view()),
    url(r"api/opt/test_upload/$", TemplateView.as_view(template_name="test_upload.html"), name="test"),

]