from events.models import Event,EventRole,Role,GroupInvitation,MemberInvitation,MemberResponse,EventType
from django.contrib import admin

#class RoleInline(admin.StackedInline):
#	model = Role
#	extra = 0
#class EventRoleInline(admin.StackedInline):
#	model = EventRole
#	extra = 0

#class MemberInvitationInline(admin.StackedInline):
#	model = MemberInvitation
#	extra = 0

#class EventAdmin(admin.ModelAdmin):
#	inlines = [EventRoleInline]
#	inlines = [GroupInvitationInline, MemberInvitationInline]
#	inlines = [RoleInline]

#class RoleInline(admin.StackedInline):
#	model = EventRole
#	extra = 0
#
#class RoleAdmin(admin.ModelAdmin):
#	inlines = [RoleInline]

class GroupInvitationInline(admin.StackedInline):
	model = GroupInvitation
	extra = 0
class MemberInvitationInline(admin.StackedInline):
	model = MemberInvitation
	extra = 0
class EventRoleAdmin(admin.ModelAdmin):
	inlines = (MemberInvitationInline,GroupInvitationInline)
###

class EventRoleInline(admin.StackedInline):
	model = EventRole
	extra = 1

class EventAdmin(admin.ModelAdmin):
	inlines = [EventRoleInline]


admin.site.register(Event, EventAdmin)
#admin.site.register(Role, RoleAdmin)
admin.site.register(Role)
admin.site.register(EventRole, EventRoleAdmin)
admin.site.register(GroupInvitation)
admin.site.register(MemberInvitation)
admin.site.register(MemberResponse)
admin.site.register(EventType)
