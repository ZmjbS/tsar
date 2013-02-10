from groups.models import Group,Membership
from django.contrib import admin

class GroupAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}

admin.site.register(Group, GroupAdmin)
admin.site.register(Membership)
