# coding=utf8
from api.cacher.base_dal import MealsBaseDAL

class MealsDal(MealsBaseDAL):
    def __init__(self, db_conn_args):
        super(MealsDal, self).__init__(db_conn_args)


