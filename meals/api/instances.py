# coding=utf-8
import settings
from api.cacher.cacher import Cacher
from api.cacher.dal import MealsDal

dal = MealsDal(settings.db_conn_args)
cacher = Cacher(dal)
