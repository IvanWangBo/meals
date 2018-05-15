#coding=utf-8

class UserAdminType(object):
    personnel = 0
    restaurant = 1
    company = 2
    admin = 3

    choices = [(personnel, u'员工'), (restaurant, u'餐厅'), (company, u'企业'), (admin, u'管理员'), ]

    valid_list = [personnel, restaurant, company, admin, ]


class UserGender(object):
    unknown = 0
    male = 1
    female = 2

    choices = [(unknown, u'未知的'), (male, u'男'), (female, u'女'), ]

    valid_list = [unknown, male, female, ]


class OrderStatus(object):
    canceled = -1
    created = 0
    accepted = 1
    sending = 2
    finished = 3
    settled = 4
