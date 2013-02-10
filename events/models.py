# -*- coding: utf-8 -*-
from django.db import models
from groups.models import Group
from members.models import Member
from django.db.models import get_model
from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import SplitDateTimeWidget

class Role(models.Model):
	title = models.CharField(max_length=64)

	def __unicode__(self):
		return self.title

class EventType(models.Model):
	title = models.CharField(max_length=64)
	description = models.TextField(blank=True)

	def __unicode__(self):
		return self.title

class Event(models.Model):
	title = models.CharField(max_length=64)
	description = models.TextField(blank=True)
	date_time_begin = models.DateTimeField()
	date_time_end = models.DateTimeField()
	#Need to implement locations. Character fields or just store this all in a GPX file?
	#Should locations be tags, or is it sufficient to filter from predefined areas and GPX files?
	event_type = models.ForeignKey(EventType)
	#Add equipment to log equipment use. Better to add this as a relation rather than a tag?

	def __unicode__(self):
		return self.title

class EventRole(models.Model):
	event = models.ForeignKey(Event)
	role = models.ForeignKey(Role)
	invited_groups = models.ManyToManyField(Group, through='GroupInvitation')
	invited_members = models.ManyToManyField(Member, through='MemberInvitation')
	minimum = models.SmallIntegerField(default=0)
	maximum = models.SmallIntegerField(default=0)

	def __unicode__(self):
		return self.event.title +' '+ self.role.title

class GroupInvitation(models.Model):
	event_role = models.ForeignKey(EventRole)
	group = models.ForeignKey(Group)
	is_hidden = models.BooleanField(default=False)

	def __unicode__(self):
		return self.event_role.__unicode__() +'>'+ self.group.title

class MemberInvitation(models.Model):
	event_role = models.ForeignKey(EventRole)
	member = models.ForeignKey(Member)
	is_hidden = models.BooleanField(default=False)

	def __unicode__(self):
		return self.event_role.__unicode__() +'>'+ self.member.user.username

#class SplitDateTimeJSField(forms.SplitDateTimeField):

class EventCreation(ModelForm):
	class Meta:
		model = Event
	title = forms.CharField(max_length=64,label='Titill:',initial='Titill')
	date_time_begin = forms.DateTimeField(input_formats={'%m/%d/%Y %H:%M'},label='Hefst:')
	date_time_end   = forms.DateTimeField(input_formats={'%m/%d/%Y %H:%M'},label='Lýkur:')
	description = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '5'}),label='',initial='Lýsing')
	event_type = forms.ModelChoiceField(queryset=EventType.objects.all(), empty_label='(ekkert)')
#	class Meta:
#		model = Event
	#TODO: Need to implement locations. Character fields or just store this all in a GPX file?
	#Should locations be tags, or is it sufficient to filter from predefined areas and GPX files?
	#TODO: Add the type after we've created the event as this should probably happen at the same stage as when we add the various tags.
	#event_type = forms.ModelChoiceField(queryset=EventType.objects.all())
	#Add equipment to log equipment use. Better to add this as a relation rather than a tag?

class EventRoleForm(ModelForm):
	class Meta:
		model = EventRole
	invited_groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())
	invited_members= forms.ModelMultipleChoiceField(queryset=Member.objects.all())
	minimum = forms.CharField(label='Fjöldi:')
	maximum = forms.CharField(label='til')
