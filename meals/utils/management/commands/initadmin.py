# coding=utf-8
from django.core.management.base import BaseCommand

from api.users.models import Users
from common.constants import UserAdminType


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("user_name: "))
        user_name = raw_input()
        try:
            admin = Users.objects.get(user_name=user_name)
            if admin.admin_type == UserAdminType.admin:
                self.stdout.write(self.style.WARNING("Super admin user '%s' already exists, "
                                                     "would you like to reset it's password?\n"
                                                     "Input yes to confirm: " % user_name))
                if raw_input() == "yes":
                    password = raw_input()
                    self.stdout.write(self.style.WARNING("password: "))
                    admin.set_password(password)
                    admin.save()
                    self.stdout.write(self.style.SUCCESS("Successfully change admin user password.\n"
                                                         "Username: %s\nPassword: %s\n" % (user_name, password)))
                else:
                    self.stdout.write(self.style.SUCCESS("Nothing happened"))
            else:
                self.stdout.write(self.style.ERROR("User %s is not super admin.\n"
                                                   "Do you want to change %s into admin ?\n"
                                                   "Input yes to confirm: " % (user_name, user_name)))
                if raw_input() == "yes":
                    admin.admin_type = UserAdminType.admin
                    admin.save()
                else:
                    self.stdout.write(self.style.SUCCESS("Nothing happened"))

        except Users.DoesNotExist:
            user = Users.objects.create(user_name=user_name, real_name=u"管理员", email="admin@meals.com", admin_type=UserAdminType.admin)
            self.stdout.write(self.style.WARNING("password: "))
            password = raw_input()
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS("Successfully created admin user.\n"
                                                 "Username: %s\nPassword: %s\n" % (user_name, password)))
