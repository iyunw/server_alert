from django.contrib import admin
from alert.models import GroupAlertServer


class GroupAlertServerAdmin(admin.ModelAdmin):
    pass


admin.site.register(GroupAlertServer, GroupAlertServerAdmin)
