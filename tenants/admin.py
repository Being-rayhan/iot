# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User
# from django.contrib.auth.models import Group
# from django.utils.translation import ugettext_lazy as _


# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'contact_number', 'is_active', 'is_staff', 'is_superuser')
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'contact_number')}),
#     )

# admin.site.register(User, CustomUserAdmin)
# admin.site.unregister(Group)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Org
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from django.contrib.admin.sites import AdminSite
# AdminSite.index_template = 'graphs/graphs.html'


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'contact_number', 'orgs', 'is_client', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('contact_number', 'is_client', 'orgs')}),
        (_('Permissions'), {'fields': ('groups', )}),
    )

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        obj.is_superuser = False
        obj.save()

admin.site.register(User, CustomUserAdmin)


class OrgAdmin(admin.ModelAdmin):
    #list_display = ('name', )
     list_display = ('num', 'test_field')

admin.site.register(Org, OrgAdmin)