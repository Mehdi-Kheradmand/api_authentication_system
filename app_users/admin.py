from django.contrib import admin
from django.contrib.auth.models import User

from app_users.models import UserAdditional
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# create a class inherited from admin.StackedInline
class UserAdditionalInline(admin.StackedInline):
    model = UserAdditional
    can_delete = False
    verbose_name_plural = 'Additional Info'


class UserAdmin(BaseUserAdmin):
    inlines = (UserAdditionalInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
