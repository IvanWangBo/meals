# coding=utf-8
from django.core.management.base import BaseCommand

from api.users.models import Users
from common.constants import UserAdminType
from common.constants import UserGender


class Cacher(object):
    def __init__(self, dal):
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

    def get_personnel_list(self, company_id):
        return self.dal._db_get_table_records(
            'users',
            ['user_name', 'real_name', 'phone_number', 'gender', 'company_id', 'department_id', ],
            where={'company_id': company_id, 'admin_type': UserAdminType.personnel, 'is_enabled': 1})

    def get_order_id(self):
        self.dal.begin()
        order_id = self.dal._db_get_table_record(
            'order_id',
            ['now_id', ],
            where={}
        )
        if not order_id:
            now_id = 1
            self.dal.insert('order_id', {'now_id': now_id + 1})
        else:
            now_id = order_id.get('now_id', 1)
            self.dal.update('order_id', {'now_id': now_id + 1}, where={'now_id': now_id})
        self.dal.commit()
        return now_id

    def get_screen_order_id(self, order_id, user_id, company_id, year, month, day, time_range):
        return '%2d%2d%2d%2d%d%3d%4d' % (company_id, year % 100, month, day, time_range, user_id, order_id)
