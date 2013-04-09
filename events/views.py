# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from members.models import Member
from groups.models import Group
from events.models import Role, EventType, Event, EventRole, EventCreation, EventRoleForm, GroupInvitation
from django.http import HttpResponseRedirect, HttpResponse

from django.utils import timezone
import datetime
from dateutil import parser

import simplejson as json
#import json

now = datetime.datetime.now()

def list_events(request):
	recent_events_list = Event.objects.filter(date_time_begin__lte=now).order_by('-date_time_begin')[:20]
	coming_events_list = Event.objects.filter(date_time_begin__gte=now).order_by('date_time_begin')[:20]
	return render_to_response('events/events_index.html', { 'recent_events_list': recent_events_list, 'coming_events_list': coming_events_list })

def display_or_save_event_form(request):
	event_types = EventType.objects.all()
	event_roles = Role.objects.all()
	members = Member.objects.all()
	groups = Group.objects.all()
	form = EventCreation(request.POST)
	#if request.method == 'POST':
	#	event_role_form = EventRoleForm(request.POST)
	#	if (form.is_valid()):
	#		form.save()
	#	return HttpResponse(json.dumps({ 'form': form, 'event_role_form': event_role_form, 'event_types': event_types, 'event_roles': event_roles, 'members': members, 'groups': groups, }))
	#else:
	return render(request, 'events/create_event.html', { 'form': form, 'event_types': event_types, 'event_roles': event_roles, 'members': members, 'groups': groups, })

#TODO: Need to find a way to differentiate between groups and members that are invited. Since the group IDs are just strings, maybe use strings on the form 'm4' and 'g4' for the fourth member and group, respectively.
#TODO: Do we need to remove orphaned invitations once an EventRole has been removed?
#TODO: Reorder these try-s to shorten them so that the exceptions make more sense.
def save_event(request):
	if request.is_ajax() or True:
		print 'Is AJAX'
		# TODO: Add handler for these below. They are required and must be submitted or else the form will not validate. Or perhaps the clean_fields() exception is enough...?
		import pprint
		print 'Hér kemur hrátt data:'
		pprint.pprint(request.POST['data'])
		print 'Hér kemur JSON útgáfan:'
		data = json.loads(request.POST['data'])
		pprint.pprint(data)
		t = data['title']
		d = data['description']
		dtb = timezone.make_aware(parser.parse(data['date_time_begin']),timezone.get_default_timezone())
		dte = timezone.make_aware(parser.parse(data['date_time_end']),timezone.get_default_timezone())
		et_id = data['event_type']
		try:
			event_id = data['event_id']
			if event_id == '':
			# If no event id has been supplied, we'll create a new event.
				event = Event(title=t, description=d, date_time_begin=dtb, date_time_end=dte, event_type_id=et_id)
			else:
			# else we update the existing one.
				event = Event.objects.get(pk=event_id)
				event.title = t
				event.description = d
				event.date_time_begin = dtb
				event.date_time_end = dte
				event.event_type_id = et_id
				#return HttpResponse('Event fields updated.')
			# Now save the event
			try:
				event.clean_fields()
				event.save()
				print 'The event is: ------'
				print (vars(event))
				print '--------------------'
			except:
				return HttpResponse ("Hello, world. Could not save event.")

			# Now that the event has been taken care of, let's sort out the event roles etc.
			# Flow:
			# For each role:
			for role in Role.objects.all():
				print 'Role ID %s' % role.id
				print 'Role is %s' % role
				try: #if we want the role:
					currentparticipants = [] # This will be populated below if the event exists (and currently has any participants).
					currentgroups= [] # This will be populated below if the event exists (and currently has any participants).

					wantedparticipantIDs = map(int,data['role'][role.id]['participants'])
					print 'Wanted participantsID: {}'.format(wantedparticipantIDs)
					#TODO: Add an option to allow for wantedparticipatns to be either groups or members. Will require some modification of the form to distinguish between member and group IDs.
					#wantedgroups = map(int,wantedparticipantIDs)
					wantedgroups = [Group.objects.get(pk=groupid) for groupid in wantedparticipantIDs]
					print 'We want event role {} with groups {}'.format(role, wantedgroups)
					try: #check whether the EventRole already exists
						# In the event that an EventRole already exists, we have to:
						#  1. Get the EventRole, stored in eventrole.
						#  2. Remove unwanted participants
						# Adding wanted participants is shared with EventRoles that
						# need to be created so we're doing that later on.

						# 1.
						eventrole = EventRole.objects.get(event_id=event.id,role_id=role.id)
						print 'EventRole "{}" already exists.'.format(eventrole)

						# 2.
						#currentgroups= GroupInvitation.objects.filter(event_role=eventrole)
						currentgroups = eventrole.invited_groups.all()
						print 'currentgroups: {}'.format(currentgroups)
						print 'EventRole already has these invitations:'
						for group in currentgroups:
							print '>>{} ({})'.format(group, group.id)
							#print 'Comare {} with {}'.format(group.id,wantedgroups)
							if group not in wantedgroups:
								print '-- ID is {}: We don\'t want {}.'.format(group.id,group)
								#gi = GroupInvitation(event_role=eventrole,group=group)
								#print 'Removing group {} from eventrole {}'.format(group,eventrole)
								#print 'DEBUG'
								try:
									print 'DEBUG: {}'.format(eventrole.invited_groups)
									gi = GroupInvitation.objects.get(event_role=eventrole,group=group)
									#print gi
									gi.delete()
									print 'BINGO'
								except:
									print 'Could not remove group {} from {}'.format(group,currentgroups)
							else:
								print '++ ID is {}: We keep {}.'.format(group.id,group)
					except: #else
						# Since there is no existing EventRole, we need to:
						#  1. Create an EventRole, and save it as eventrole.
						# and that's it! Adding participants is done below for both
						# existing and recently created EventRoles.
						eventrole = EventRole(event_id=event.id,role_id=role.id,minimum=int(data['role'][role.id]['min']), maximum=int(data['role'][role.id]['max']))
						print 'No EventRole exists, creating {}.'.format(eventrole)
						try:
							eventrole.clean_fields()
							eventrole.save()
							print 'eventrole saved: {}.'.format(eventrole)
						except:
							return HttpResponse('Hello, world. Could not save eventrole.')

					# Now that we have the eventrole and it has been stripped of its
					# unwanted participatns, let's add the wanted ones.
					# Workflow:
					# For each wanted participant,
					#   if they're not currently invited,
					#     create a GroupInvitation and attach it to the EventRole

					# For each participant
					print 'Adding invitations:'
					print 'Wanted groups: {}'.format(wantedgroups)
					for group in wantedgroups:
						print '>>{} ({})'.format(group, group.id)
						if group not in currentgroups:
							print '++ Group {} is not invited: Create GroupInvitation!'.format(group)
							gi = GroupInvitation(event_role=eventrole, group=group)
							print '++ GroupInvitation created: '.format(gi)
							try:
								gi.clean_fields()
								gi.save()
								print '++ GroupInvitation saved'
							except:
								print 'ERROR: Could not save GroupInvitation {}'.format(gi)
						else:
							print '.. Group {} already invited: nothing to do. :-)'.format(group)
					print 'All done!'
				except: #if we don't want the role:
					print 'No role wanted.'
					try: # check if the role exists and must be removed
						eventrole = EventRole.objects.get(event__id=event.id,role__id=role.id)
						print 'Removing eventrole: %s' % eventrole
						eventrole.delete()
					except: # No role wanted. No role exists. All good.
						print 'No role exists. All good.'
				print ' ..... '
		except:
			return HttpResponse("Hello, world. Could not create event.")
		return HttpResponse(event.id)
	else:
		return HttpResponse("Hello, world. Not AJAX request.")

def group_save(request):
	if request.is_ajax():
		eventId = request.POST['eid']
		roleId = request.POST['rid']
		group = request.POST['grp']
		member = request.POST['grp']
		mininum = request.POST['min']
		maximum = request.POST['max']
	else:
		# Perhaps just merge this with the standard view response.
		return HttpResponse("Group save request isn't an AJAX request.")
