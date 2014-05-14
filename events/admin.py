from events.models import Event,EventRole,Role,GroupInvitation,MemberInvitation,PositionInvitation,MemberResponse,EventType,MemberAttendance,EventTag,Tag,TagType
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
class PositionInvitationInline(admin.StackedInline):
	model = PositionInvitation
	extra = 0
class EventRoleAdmin(admin.ModelAdmin):
	inlines = (MemberInvitationInline,GroupInvitationInline,PositionInvitationInline)
###

class EventRoleInline(admin.StackedInline):
	model = EventRole
	extra = 1

class EventTagsInline(admin.StackedInline):
	model = EventTag
	extra = 1

class EventAdmin(admin.ModelAdmin):
	inlines = (EventRoleInline,EventTagsInline)

class EventTagInline(admin.StackedInline):
	model = EventTag
	extra = 1

#class TagTypeAdmin(admin.ModelAdmin):
	#inlines = [EventTagInline]

class AttendanceAdmin(admin.ModelAdmin):
	list_display = ('event_role', 'member', 'attendance', 'time_checkin', 'time_checkout')

class EventTypeAdmin(admin.ModelAdmin):
    list_display = ["title", "color",]
    list_editable = ["color",]

admin.site.register(Event, EventAdmin)
#admin.site.register(Role, RoleAdmin)
admin.site.register(Role)
admin.site.register(EventRole, EventRoleAdmin)
admin.site.register(PositionInvitation)
admin.site.register(GroupInvitation)
admin.site.register(MemberInvitation)
admin.site.register(MemberResponse)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(TagType)#,TagTypeAdmin)
admin.site.register(EventTag)
admin.site.register(Tag)
admin.site.register(MemberAttendance, AttendanceAdmin)
