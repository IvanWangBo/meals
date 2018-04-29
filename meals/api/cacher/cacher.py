# coding=utf-8
from django.core.management.base import BaseCommand

from api.users.models import Users
from common.constants import UserAdminType
from common.constants import UserGender


class Cacher(object):
    def __init__(self, dal=None):
        self.dal = dal

    def create_user(self, user_name, password, real_name="", email="", admin_type=UserAdminType.personnel, phone_number="", gender=UserGender.unknown, company_id=0, department_id=0, is_enabled=1):
        try:
            user = Users.objects.create(
                user_name=user_name,
                email=email,
                real_name=real_name,
                admin_type=admin_type,
                phone_number=phone_number,
                gender=gender,
                company_id=company_id,
                department_id=department_id,
                is_enabled=is_enabled,
            )
            user.set_password(password)
            user.save()
            return user
        except Exception as err:
            print err # todo 把print改成log的形式
            return None