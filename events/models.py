# -*- coding: utf-8 -*-
from django.db import models
from groups.models import Group
from members.models import Member, Position
from django.db.models import get_model
import datetime
from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import SplitDateTimeWidget
from paintstore.fields import ColorPickerField

class Role(models.Model):
	# Roles for participants in an event. (e.g. driver, organiser, instructor,
	# etc.).

	title = models.CharField(max_length=64)

	def __unicode__(self):
		return self.title

class EventType(models.Model):
	# Events may be of several different types that one may like to distinguish
	# between (e.g. exercise, course, meeting, social, etc.).
	#
	# TagTypes also have EventTypes as an exercise may have different tags to a
	# meeting.

	title = models.CharField(max_length=64)
	description = models.TextField(blank=True)
	color = ColorPickerField(default="#ffffff")

	def __unicode__(self):
		return self.title

class TagType(models.Model):
	# TagTypes group tags by type such as organiser, task, conditions, equipment
	# etc.
	#
	# A TagType is associated with one or more EventTypes to which it applies.
	# Most event types will have an organiser but different event types will have
	# different tasks.

	title = models.CharField(max_length=64)
	event_type = models.ManyToManyField(EventType)

	def __unicode__(self):
		return self.title + ": " + ", ".join([et.title for et in self.event_type.all()])

class Tag(models.Model):
	# Events have Tags for analysis. These should be chosen depending on which
	# elements should be focused on in each type of event. Exercises could for
	# example be tagged with first-aid, avalanche rescue or similar techniques.
	#
	# Tags are grouped into TagTypes (e.g. organiser, task, conditions, equipment,
	# etc.).
	title = models.CharField(max_length=64)
	tag_type = models.ForeignKey(TagType)

	def __unicode__(self):
		return self.title
		  
class Event(models.Model):
	# The fundamental object. Most of the magic happens in EventRole, however.
	#
	# An event may have several roles and members can be invited to one or more
	# roles, either as members, or through groups which they belong to.
	#
	# Events come in various types, have locations and can be tagged with
	# techniques employed or something similar that will aid in analysing events.

	title = models.CharField(max_length=64)
	description = models.TextField(blank=True)
	date_time_begin = models.DateTimeField()
	date_time_end = models.DateTimeField()
	event_type = models.ForeignKey(EventType)
	tags = models.ManyToManyField(Tag, through='EventTag', related_name='tag_events', blank=True, null=True)

	def invited_roles(self, member):
		# Returns a list of roles a member is invited to.

		invitedroles = []
		#print self.eventrole_set.all()
		for eventrole in self.eventrole_set.all():
			if eventrole.is_open:
				invitedroles.append(eventrole)
			for position in eventrole.invited_positions.all():
				if member in position.member_set.all() and eventrole not in invitedroles:
					invitedroles.append(eventrole)
			for group in eventrole.invited_groups.all():
				if member in group.members.all() and eventrole not in invitedroles:
					invitedroles.append(eventrole)
			if member in eventrole.invited_members.all() and eventrole not in invitedroles:
				invitedroles.append(eventrole)
		return invitedroles

	def responded_roles(self, member):
		# Returns a list of roles a member has responded to.

		respondedroles = []
		for eventrole in self.eventrole_set.all():
			if member in eventrole.responses.all():
				respondedroles.append(eventrole)
		return respondedroles

	#def event_roles (self):
	#	eventroles = []
	#	for eventrole self.eventrole_set.all().
	#		eventroles.append(eventrole)
	#	return eventroles

	# TODO: Need to implement locations. Character fields or just store this all in a GPX file?
	# TODO: Add equipment to log equipment use. Better to add this as a relation rather than a tag?

	def __unicode__(self):
		return self.title

class EventTag(models.Model):
	event = models.ForeignKey(Event)
	tag = models.ForeignKey(Tag)

	def __unicode__(self):
		return self.event.title +' <-> '+ self.tag.title

class EventRole(models.Model):
	# An event may have several roles, and the same group or member may be
	# invited to each of these. So for each role on each event we need an
	# “event role” to which we'll hang the invitations.
	#
	# These EventRoles are associated with:
	# * an event
	# * a role
	# * (optionally) one or more groups through GroupInvitation
	# * (optionally) one or more members through MemberInvitation
	# * (optionally) one or more positions through PositionInvitation
	# * a boolean field indicating whether the event is open to all members
	# * (optionally) one or more members through their responses to the event
	# EventRoles furthermore have:
	# * an optional maximum number of members allowed
	# * an optional minimum number of members required
	# * a boolean indicating whether the role details should be hidden to non-invited members

	event = models.ForeignKey(Event)
	role = models.ForeignKey(Role)
	invited_groups = models.ManyToManyField(Group, through='GroupInvitation', blank=True, null=True)
	invited_members = models.ManyToManyField(Member, through='MemberInvitation', related_name='eventrole_invitations', blank=True, null=True)
	invited_positions = models.ManyToManyField(Position, through='PositionInvitation', blank=True, null=True)
	is_open = models.BooleanField(default=False)
	responses = models.ManyToManyField(Member, through='MemberResponse', related_name='eventrole_responses', blank=True, null=True)
	minimum = models.SmallIntegerField(default=0)
	maximum = models.SmallIntegerField(default=0)
	is_hidden = models.BooleanField(default=False)

	def invited(self, member):
		# Returns boolean depending on whether the member is invited to the event.
		# TODO: Unused?

		for position in self.invited_positions.all():
			if member in position.members.all():
				return True
		for group in self.invited_groups.all():
			if member in group.members.all():
				return True
		if member in self.invited_members.all():
			return True
		return False

	def response(self, member):
		# Returns the member's response to the event, unless there is none in
		# which case the response is the string 'U'.

		try:
			mr = MemberResponse.objects.get(event_role=self,member=member)
			#print 'XXX',mr.response
			return mr.response
		except:
			#print 'XXX NO RESPONSE'
			return 'U'

	def __unicode__(self):
		return self.event.title +' '+ self.role.title

class PositionInvitation(models.Model):
	# An intermediary model between an event role and a position.

	event_role = models.ForeignKey(EventRole)
	position = models.ForeignKey(Position)

	def __unicode__(self):
		return self.event_role.__unicode__() +'>'+ self.position.title

class GroupInvitation(models.Model):
	# An intermediary model between an event role and a group.

	event_role = models.ForeignKey(EventRole)
	group = models.ForeignKey(Group)

	def __unicode__(self):
		return self.event_role.__unicode__() +'>'+ self.group.title

class MemberInvitation(models.Model):
	# An intermediary model between an event role and a member.

	event_role = models.ForeignKey(EventRole)
	member = models.ForeignKey(Member)

	def __unicode__(self):
		return self.event_role.__unicode__() +'>'+ self.member.user.username

class MemberResponse(models.Model):
	# An intermediary model between an event role and a member.
	#
	# The MemberResponse details the response (whether the member is attending or
	# will be absent) and the time of the response (important for roles which
	# have a maximum number of slots).

	event_role = models.ForeignKey(EventRole)
	member = models.ForeignKey(Member)
	EVENT_RESPONSES = (
		(u'Y',u'Attending'),
		(u'N',u'Absent'),
		(u'U',u'Unclear'),
	)
	response = models.CharField(max_length=1, choices=EVENT_RESPONSES)
	# TODO: Should we add this to help gather a bit of data on member event response behaviour or is it a bit to Big-Brothery?
	#prior = models.CharField(max_length=1, choices=EVENT_RESPONSES, blank=True)
	time_responded = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.event_role.__unicode__() +'>'+ self.member.user.username

class MemberAttendance(models.Model):
	event_role = models.ForeignKey(EventRole)
	member = models.ForeignKey(Member)
	EVENT_ATTENDANCE = (
		(u'Y',u'Attended'),
		(u'N',u'Absent'),
	)
	attendance = models.CharField(max_length=1, choices=EVENT_ATTENDANCE)
	time_checkin = models.DateTimeField(blank=True, null=True)
	time_checkout = models.DateTimeField(blank=True, null=True)

	def get_attending(self, idnumber):
		print idnumber
		#attend = self.objects.exists(member_id = ids)
		return idnumber

	def __unicode__(self):
		return u'%s %s %s %s %s' % (self.event_role, self.member, self.attendance, self.time_checkin, self.time_checkout)

class EventCreation(ModelForm):
	class Meta:
		model = Event
	title = forms.CharField(max_length=64,label='Titill:',initial='Titill', widget=forms.TextInput(attrs={'placeholder': 'Titill viðburðar'}))
	date_time_begin = forms.DateTimeField(input_formats={'%m/%d/%Y %H:%M'},label='Hefst:', widget=forms.TextInput(attrs={'placeholder': 'Upphaf'}))
	date_time_end   = forms.DateTimeField(input_formats={'%m/%d/%Y %H:%M'},label='Lýkur:', widget=forms.TextInput(attrs={'placeholder': 'Lok'}))
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
