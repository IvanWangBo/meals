"""meals URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import settings
from django.conf.urls import url
from django.contrib import admin
from api.users.views import LoginView
from api.users.views import LogoutView
from django.views.generic import TemplateView

urlpatterns = [
    #url(r'^admin/', admin.site.urls),

    # html
    url(r'^login/$', TemplateView.as_view(template_name="login.html"), name="user_login_page"),
    url(r'^personnel/$', TemplateView.as_view(template_name="personnel/index.html"), name="personnel_index_page"),
    url(r'^admin/$', TemplateView.as_view(template_name="admin/index.html"), name="admin_index_page"),
    url(r'^company/$', TemplateView.as_view(template_name="company/index.html"), name="company_index_page"),
    url(r'^restaurant/$', TemplateView.as_view(template_name="restaurant/index.html"), name="restaurant_index_page"),

    # api
    url(r'^api/login/$', LoginView.as_view()),
    url(r'^api/logout/$', LogoutView.as_view()),
]