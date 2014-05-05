from members.models import *
from django.contrib import admin

class PhoneInline(admin.StackedInline):
	model = Phone
	extra = 0

class EmailInline(admin.StackedInline):
	model = Email
	extra = 0

class MemberAdmin(admin.ModelAdmin):
	inlines = [PhoneInline, EmailInline]

admin.site.register(Member, MemberAdmin)
admin.site.register(Position)
