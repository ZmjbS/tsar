# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from members.models import Member, Position
from groups.models import Group
from events.models import Role, EventType, Event, EventRole, EventCreation, EventRoleForm, PositionInvitation, GroupInvitation, MemberInvitation, MemberResponse, TagType, Tag, EventTag
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import datetime
from dateutil import parser

import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
#import json

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def calendar_events_list(member_id, start, end):
	# Get all events between the two dates.

	#print 'Retrieve events between {} and {}'.format(start, end)
	#print member_id
	member = Member.objects.get(id=member_id)
	#print member

	import calendar

	calendar_begins = datetime.fromtimestamp(int(start))
	calendar_ends = datetime.fromtimestamp(int(end))
	print 'The calendar runs from {} to {}'.format(calendar_begins, calendar_ends)

	events = Event.objects.filter(date_time_end__gt=calendar_begins).filter(date_time_begin__lt=calendar_ends)
	events_list = []
	for event in events:
		eventtype = event.event_type.title
#		print eventtype

		# Finall indicate the member's response status to each event.
		try:
			if MemberResponse.objects.get(event_role__event=event, member=member, response='Y'):
				status='attending'
		except:
#			print 'no yes'
			try:
#				print MemberResponse.objects.get(event_role__event=event, member=member, response='N')
				status = 'absent'
			except:
#				print 'no no'
#				print event
#				print member
#				print event.invited_roles(member)
				if event.invited_roles(member) != []:
					status = 'unclear'
				else:
#					print 'Not invited'
					status = 'notinvited'
#		print status

		events_list.append({
			'title': event.title,
			'start': calendar.timegm(event.date_time_begin.utctimetuple()),
			'end': calendar.timegm(event.date_time_end.utctimetuple()),
			'id': event.id,
			'url': '/vidburdur/'+str(event.id),
 			'backgroundColor': event.event_type.color,
			# Let's also send some data to display the attendance status:
			'status': status,
		})
#	import pprint
#	pprint.pprint(events_list)
	return HttpResponse(json.dumps(events_list), mimetype='application/javascript')
#	print 'FINISHED'

def list_events(request):
	if request.is_ajax():
		# Prepare events for calendar
		return calendar_events_list(request.GET['member_id'], request.GET['start'], request.GET['end'])

	# Otherwise it's just a normal request for the events page.
	now = datetime.now()
	recent_events_list = Event.objects.filter(date_time_begin__lte=now).order_by('-date_time_begin')[:20]
	coming_events_list = Event.objects.filter(date_time_begin__gte=now).order_by('date_time_begin')[:20]
	#import pprint
	#pprint.pprint(coming_events_list)
	# TODO: Add incidents?
	# recent_incidents_list = Incident.objects.filter(date_time_begin__lte=now).order_by('-date_time_begin')[:20]
	return render_to_response('events/events_index.html', {
		'recent_events_list': recent_events_list,
		'coming_events_list': coming_events_list,
		'user': request.user,
	})

@csrf_exempt
def event_response(request):
	# Receives data with information about which MemberResposne must be modified
	# or created. For this we need:
	#	. the member_id
	#	. the eventrole_id
	#	. the action
	# If the member_id is missing, we use the currently logged on member.
	# TODO: Perhaps it's better to always pass the member_id on with the other two from the view...

	print 'in event_response'
	# Ensure we're getting an AJAX POST.
	if not request.is_ajax():
		print 'not AJAX'
		return False

	print 'check member'
	# Check whether we've been handed a member_id:
	try:
		member_id = request.POST['member_id']
		cm_responding = False
		print 'member_id sent through post: {}'.format(member_id)
	except:
		member_id = request.user.member.id
		cm_responding = True
		print 'member_id set to current member'

	# Get the eventrole_id and action:
	print 'get eventrole_id'
	print request.POST
	eventrole_id = request.POST['eventrole_id']
	print 'eventrole_id: {}'.format(eventrole_id)
	action = request.POST['action']
	if action == 'attend':
		act = 'Y'
	elif action == 'absent':
		act = 'N'

	print 'action: {} or {}'.format(action,act)
	print 'eventrole.id: {}'.format(eventrole_id)

	# Get the relevant objects:
	member = Member.objects.get(id=member_id)
	event_role = get_object_or_404(EventRole, id=eventrole_id)
	#event_role = EventRole.objects.get(event_role__id=eventrole_id)

	# See if there already exists a member response:
	try:
		mr = MemberResponse.objects.get(event_role=event_role, member=member)
		print '>> MemberResponse {} found'.format(mr)
		mr.response=act
		mr.time_responded=datetime.now()
	# Otherwise create a new one:
	except:
		mr = MemberResponse(event_role=event_role, member=member, response=act)
		print '>> No MemberResponse found. Creating a new one: {}'.format(mr)

	# Clean and save:
	try:
		mr.clean_fields()
		mr.save()
		print '>> SAVED'
	except:
		print '>> FAILED'
		return HttpResponse('Failed: could not save member response')

	##print 'Hér kemur JSON útgáfan:'
	##data = json.loads(request.POST['data'])
	##pprint.pprint(data)

	print mr.time_responded
	data = {
		'user_id': member.user.id,
		'user_name': member.__unicode__(),
		'username': member.user.username,
		'cm_responding': cm_responding,
		'event_id': event_role.event.id,
		'role_id': event_role.role.id,
		'eventrole_id': event_role.id,
		'action': action,
		'time_responded': mr.time_responded,
	}
	print 'Data: {}'.format(data)
	jsondata = json.dumps(data, cls=DjangoJSONEncoder)
	print 'JSON: ',jsondata
	print 'XXXXX responding'
	#return HttpResponse(json.dumps(data))##, mimetype='application/javascript')
	return HttpResponse(jsondata)

from django.contrib.auth.decorators import login_required
@login_required
def display_event(request, pk):

	print 'beginning def'
	event = get_object_or_404(Event.objects.select_related('eventtype', 'eventrole_set', 'tags'), id=pk)
	cm = request.user.member
	# Compile a list of members who are invited.
	# Workflow:
	# Create an empty list of invited members.
	# For each role
	#	for each invited position
	#		for each member
	#			if member is not on the invited list
	#				add member to the list
	#	for each invited group
	#		for each member
	#			if member is not on the invited list
	#				add member to the list
	#	for each invited member
	#		if member is not on the invited list
	#			add member to the list
	role_data = []
	
	total_attending = set()
	total_absent    = set()
	total_unclear   = set()

	for eventrole in EventRole.objects.filter(event=event):
	#	print 'On EventRole {}:'.format(eventrole)
		attending = []
		absent = []
		unclear = []
		attending_responses = []
		absent_responses = []

		# First populate those attending or absent from existing responses.
		for memberresponse in eventrole.memberresponse_set.all():
#			print '> memberresponse: {}'.format(memberresponse)
			if memberresponse.response == 'Y':
				attending.append(memberresponse.member)
				attending_responses.append(memberresponse)
			if memberresponse.response == 'N':
				absent.append(memberresponse.member)
				absent_responses.append(memberresponse)
#		print '> Attending members {}:'.format(attending)
#		print '> Absent members: {}'.format(absent)

		# Run through those who are invited but whose status is still unclear.
		if eventrole.is_open:
		# If it's an open event, check all members.
			for member in Member.objects.all():
				if member not in attending and member not in absent:
					unclear.append(member)
		else:
		# If it isn't an open event, check invited members:
#			print '>> Members invited through positions'
			for member in Member.objects.filter(position__eventrole=eventrole):#filter(group__groupinvitation__event_role__event=event):
#				print '>>   {}'.format(member.user.username)
				if member not in unclear and member not in attending and member not in absent:
					unclear.append(member)
#					print '++   {}'.format(member)
#			print '>> Members invited through groups'
			for member in Member.objects.filter(group__groupinvitation__event_role=eventrole):#filter(group__groupinvitation__event_role__event=event):
#				print '>>   {}'.format(member.user.username)
				if member not in unclear and member not in attending and member not in absent:
					unclear.append(member)
#					print '++   {}'.format(member)
#			print '>> Members invited directly'
			for member in Member.objects.filter(memberinvitation__event_role=eventrole):#filter(memberinvitation__event_role__event=event):
#				print '>>   {}'.format(member)
				if member not in unclear and member not in attending and member not in absent:
					unclear.append(member)
#					print '++   {}'.format(member)

		# Add these to the total:
		total_attending.update(attending)
#		print 'Total attending: {}'.format(total_attending)
		total_absent.update(absent)
		total_unclear.update(unclear)

		# Check to see whether the current member has responded or is invited to a particular role.
		cm_status = 'not invited'
		if cm in unclear:
			cm_status = 'unclear'
		if cm in absent:
			cm_status = 'absent'
		if cm in attending:
			cm_status = 'attending'

		role_data.append({
			'eventrole': eventrole,
			'unclearmembers': unclear,
			'absentmembers': absent,
			'attendingmembers': attending,
			'cm_status': cm_status,
			'attending_responses': attending_responses,
			'absent_responses': absent_responses,
			})

	# Pass possible roles and event types so that we can edit the event.
	event_types = EventType.objects.all()
	#print 'EVNTTYPES: {}'.format(event_types)
	#for etype in event_types:
		#print etype.title
		#print etype.pk
	event_roles = Role.objects.all()
	#print 'EVENTROLES: {}'.format(event_roles)

# TODO: Currently members can sign up for multiple roles. This is probably a good thing as members may be both a driver and participant and we want to log each role.
#	# Now let's make sure that a member who is attending a role doesn't get invited
#	# to others.
#	# TODO: Perhaps we should implement a way of attending more than one role.
#	# Perhaps a pop-up to allow members to split their time among the roles.
#	for role in role_data:
#		if role['cm_status'] == 'attending':
#			for tmprole in role_data:
#				if tmprole['cm_status'] == 'invited' or tmprole['cm_status'] == 'absent':
#					tmprole['cm_status'] = 'attending elsewhere'
#			role['cm_status'] = 'attending'
	#import pprint
	#pprint.pprint(role_data)

	# Clear those attending one role from those absent so that the numbers accurately reflect this:
	total_absent = total_absent.difference(total_attending)
	# Clear those attending or absent from a role from those unclear so that the numbers accurately reflect this:
	total_unclear = total_unclear.difference(total_attending)
	total_unclear = total_unclear.difference(total_absent)

	# Pass possible tag types so that we can edit the event.
	tagtypes = TagType.objects.all()

	# Generate position, group and member lists for the selection.
	positions = []
	for position in Position.objects.select_related(depth=0).all():
		positions.append({ 'title': position.title, 'id': position.id, })
	groups = []
	for group in Group.objects.select_related(depth=0).all():
		groups.append({ 'title': group.title, 'id': group.id, })
	members = []
	for member in Member.objects.select_related(depth=0).all():
		members.append({ 'name': member.__unicode__(), 'id': member.id, })

	print 'returning data to view'

	return render_to_response('events/event_page.html', {
		'user': request.user,
		'event': event,
		'cm': cm,
		'role_data': role_data,
		'status_list': ['attending', 'absent', 'unclear'],
		'event_types': event_types,
		'event_roles': event_roles,
		'total_attending': len(total_attending),
		'total_absent': len(total_absent),
		'total_unclear': len(total_unclear),
		'tagtypes': tagtypes,
		'positions': positions, 'members': members, 'groups': groups,
	})

def display_event_form(request):
	event_types = EventType.objects.all()
	event_roles = Role.objects.all()
	positions = Position.objects.all()
	members = Member.objects.all()
	groups = Group.objects.all()
	form = EventCreation(request.POST)
	tagtypes = TagType.objects.all()
	#if request.method == 'POST':
	#	event_role_form = EventRoleForm(request.POST)
	#	if (form.is_valid()):
	#		form.save()
	#	return HttpResponse(json.dumps({ 'form': form, 'event_role_form': event_role_form, 'event_types': event_types, 'event_roles': event_roles, 'members': members, 'groups': groups, }))
	#else:
	return render(request, 'events/create_event.html', {
				'form': form,
				'event_types': event_types,
				'event_roles': event_roles,
				'positions': positions, 'members': members, 'groups': groups,
				'tagtypes': tagtypes,
			  })

#TODO: Do we need to remove orphaned invitations once an EventRole has been removed?
def save_event(request):
	print 'Saving event'
	if not request.is_ajax():
		return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Hello, world. Not an AJAX request.'}))
	else:
		print 'Is AJAX'
		import pprint
		print 'Hér kemur hrátt data:'
		pprint.pprint(request.POST['data'])
		print 'Hér kemur JSON útgáfan:'
		data = json.loads(request.POST['data'])
		pprint.pprint(data)

		# Sanitise some of the data and return messages if it fails.

		### TITLE ###
		# The title must be non-zero and no longer than 64 characters (defined in events/models.py).
		print 'Submitted data:'
		t = data['title']
		if t == "":
			return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Title missing.', }))
		elif len(t) > 64:
			return HttpResponse(json.dumps({ 'type': 'error', 'message': 'The title is currently '+str(len(t))+' characters long but the maximum is 64.', }))
		import sys
		print sys.stdout.encoding
		print type(t)
		print '--title: {}'.format(t.encode('UTF-8'))

		### DESCRIPTION ###
		# There are no restrictions on the description field other than being cleaned. It may be blank and arbitrarily long.
		d = data['description']
		# The dates must be supplied and the beginning must precede the end.
		print '--description: {}'.format(d.encode('UTF-8'))

		### DATES ###
		if data['date_time_begin'] == "":
			return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Beginning date missing.', }))
		try:
			dtb = timezone.make_aware(parser.parse(data['date_time_begin']),timezone.get_default_timezone())
		except:
			return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Beginning date-time is not a valid datetime.', }))
		print '--begins: {}'.format(dtb)
		if data['date_time_end'] == "":
			return HttpResponse(json.dumps({ 'type': 'error', 'message': 'End date missing.', }))
		try:
			dte = timezone.make_aware(parser.parse(data['date_time_end']),timezone.get_default_timezone())
		except:
			return HttpResponse(json.dumps({ 'type': 'error', 'message': 'End date-time is not a valid datetime', }))
		if dte <= dtb:
			return HttpResponse(json.dumps({ 'type': 'error', 'message': 'The event start time must precede the end.', }))
		print '--ends: {}'.format(dte)

		### TYPE ###
		# The event-type must be supplied.
		et_id = data['event_type']
		print '--type ID: {}'.format(et_id)
		if et_id== "":
			return HttpResponse(json.dumps({ 'type': 'error', 'message': 'No event type supplied.', }))

		### EVENT ID ###
		print 'All the data has been submitted. Checking whether event_id has been supplied.'
		try:
			event_id = data['event_id']
			print 'event_id: {}'.format(event_id)
		except:
			return HttpResponse(json.dumps({ 'type': 'error', 'message': 'No event_id submitted.', }))
		if event_id == '':
			# If no event id has been supplied, we'll create a new event.
			print 'Creating event...'
			event = Event(title=t, description=d, date_time_begin=dtb, date_time_end=dte, event_type_id=et_id)
		else:
			# else we update the existing one.
			print 'Updating event...'
			event = Event.objects.get(pk=event_id)
			event.title = t
			event.description = d
			event.date_time_begin = dtb
			event.date_time_end = dte
			event.event_type_id = et_id

		# Now save the event
		try:
			event.clean_fields()
			event.save()
			print 'The event is: ------'
			pprint.pprint(vars(event))
			print '--------------------'
		except:
			return HttpResponse (json.dumps({ 'type': 'error', 'message': 'Could not save event.'}))

		# Now that the event has been taken care of, let's sort out the event roles etc.
		# Flow:
		# For each role:
		for role in Role.objects.all():
			print 'Role ID %s' % role.id
			print 'Role is %s' % role
			try:
				participants_exist = data['role'][role.id]['participants']
			except:
				participants_exist = False
			#print participants_exist
			if participants_exist:
				# If we want eventroles, check whether these need to be created and otherwise update them.

				currentparticipants = [] # This will be populated below if the event exists (and currently has any participants).
				currentgroups = [] # This will be populated below if the event exists (and currently has any participants).
				currentmembers= [] # This will be populated below if the event exists (and currently has any participants).

				# The wantedparticipantIDs is a list of invitations compiled from a
				# drop-down in the interface. the drop-down contains positions,
				# groups, members and the option to make it an open event (inviting
				# all members). To differentiate between the primary keys of
				# positions, groups and members, these are prefixed with the
				# characters 'p', 'g' and 'm', respectively.

				wantedparticipantIDs = data['role'][role.id]['participants']
				print 'Wanted participantsID: {}'.format(wantedparticipantIDs)

				wantedpositions = [Position.objects.get(pk=int(positionid[1:])) for positionid in wantedparticipantIDs if positionid[0]=='p']
				print 'We want event role {} with positions {}'.format(role, wantedpositions)
				wantedgroups = [Group.objects.get(pk=int(groupid[1:])) for groupid in wantedparticipantIDs if groupid[0]=='g']
				print 'We want event role {} with groups {}'.format(role, wantedgroups)
				wantedmembers= [Member.objects.get(pk=int(memberid[1:])) for memberid in wantedparticipantIDs if memberid[0]=='m']
				print 'We want event role {} with members {}'.format(role, wantedmembers)

				# Check whether the event is open.
				is_open = ('a' in wantedparticipantIDs)

				# Workflow:
				#  1. Get or create the EventRole.
				#  2. Remove unwanted invitations.
				#  3. Update the minimum and maximum number of participants.
				#  4. Adding wanted invitations

				try: # check whether the EventRole already exists
					# 1. Get the EventRole, stored in eventrole.
					eventrole = EventRole.objects.get(event_id=event.id,role_id=role.id)
					print 'EventRole "{}" already exists.'.format(eventrole)
				except:
					# Since there is no existing EventRole, we need to:
					#  1. Create an EventRole, and save it as eventrole.
					# and that's it! Adding participants is done below for both
					# existing and recently created EventRoles.
					try:
						print 'event_id: {}'.format(event.id)
						print 'role_id: {}'.format(role.id)
						# TODO: Later feature...
						#eventrole = EventRole(event_id=event.id,role_id=role.id,minimum=int(data['role'][role.id]['min']), maximum=int(data['role'][role.id]['max']))
						eventrole = EventRole(event_id=event.id,role_id=role.id,is_open=is_open)
						print 'No EventRole exists, creating {}.'.format(eventrole)
					except:
						print 'Could not create eventrole.'
						return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Could not create eventrole.' }))
					try:
						eventrole.clean_fields()
						eventrole.save()
						print 'eventrole saved: {}.'.format(eventrole)
					except:
						return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Could not save eventrole.' }))

				# 2. Remove unwanted invitations.
				currentpositions = eventrole.invited_positions.all()
				currentgroups = eventrole.invited_groups.all()
				currentmembers= eventrole.invited_members.all()
				print 'currentpositions: {}'.format(currentpositions)
				print 'currentgroups: {}'.format(currentgroups)
				print 'currentmembers: {}'.format(currentmembers)
				print 'EventRole already has these invitations:'
				for position in currentpositions:
					print '>>{} ({})'.format(position, position.id)
					if position not in wantedpositions:
						print '-- ID is {}: We don\'t want {}.'.format(group.id,group)
						try:
							#print 'DEBUG: {}'.format(eventrole.invited_positions)
							pi = PositionInvitation.objects.get(event_role=eventrole,position=position)
							pi.delete()
						except:
							print 'Could not remove position {} from {}'.format(group,currentgroups)
							return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Could not remove position '+str(position)+' from '+currentpositions+'.' }))
					else:
						print '++ ID is {}: We keep position {}.'.format(position.id,position)
				for group in currentgroups:
					print '>>{} ({})'.format(group, group.id)
					if group not in wantedgroups:
						print '-- ID is {}: We don\'t want {}.'.format(group.id,group)
						try:
							#print 'DEBUG: {}'.format(eventrole.invited_groups)
							gi = GroupInvitation.objects.get(event_role=eventrole,group=group)
							gi.delete()
						except:
							print 'Could not remove group {} from {}'.format(group,currentgroups)
							return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Could not remove group '+str(group)+' from '+currentgroups+'.' }))
					else:
						print '++ ID is {}: We keep group {}.'.format(group.id,group)
				for member in currentmembers:
					print '>>{} ({})'.format(member, member.id)
					if member not in wantedmembers:
						print '-- ID is {}: We don\'t want {}.'.format(member.id,member)
						try:
							#print 'DEBUG: {}'.format(eventrole.invited_members)
							mi = MemberInvitation.objects.get(event_role=eventrole,member=member)
							mi.delete()
						except:
							print 'Could not remove member {} from {}'.format(member,currentmembers)
							return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Could not remove member '+str(member)+' from '+currentmembers+'.' }))
					else:
						print '++ ID is {}: We keep member {}.'.format(member.id,member)

				# Finally set whether the EventRole is open to all members:
				eventrole.is_open = is_open
				try:
					eventrole.clean_fields()
					eventrole.save()
					print 'eventrole saved: {}.'.format(eventrole)
				except:
					return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Could not update whether the EventRole is open numbers.' }))

				# 3. Update the minimum and maximum number of participants.
				# TODO: Later feature...
				#if eventrole.minimum != int(data['role'][role.id]['min']) or eventrole.maximum != int(data['role'][role.id]['max']):
				#	eventrole.minimum = int(data['role'][role.id]['min'])
				#	eventrole.maximum = int(data['role'][role.id]['max'])
				#	try:
				#		eventrole.clean_fields()
				#		eventrole.save()
				#		print 'eventrole saved: {}.'.format(eventrole)
				#	except:
				#		return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Could not update eventrole max/min numbers.' }))

				# 4. Adding wanted invitations
				# Now that we have the eventrole and it has been stripped of its
				# unwanted participatns, let's add the wanted ones.
				# Workflow:
				# For each wanted participant,
				#   if they're not currently invited,
				#     create a {Position,Group,Member}Invitation and attach it to the EventRole

				# For each participant
				print 'Adding invitations:'
				print 'Wanted positions: {}'.format(wantedpositions)
				print 'Wanted groups: {}'.format(wantedgroups)
				print 'Wanted members: {}'.format(wantedmembers)
				for position in wantedpositions:
					print '>>{} ({})'.format(position, position.id)
					if position not in currentpositions:
						print '++ Position {} is not invited: Create PositionInvitation!'.format(position)
						print eventrole
						print position
						pi = PositionInvitation(event_role=eventrole, position=position)
						print '++ PositionInvitation created: '.format(pi)
						try:
							pi.clean_fields()
							pi.save()
							print '++ PositionInvitation saved'
						except:
							print 'ERROR: Could not save PositionInvitation {}'.format(pi)
							return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Could not save PositionInvitation '+pi+'.' }))
					else:
						print '.. Position {} already invited: nothing to do. :-)'.format(position)
				print 'Positions done!'
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
							return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Could not save GroupInvitation '+gi+'.' }))
					else:
						print '.. Group {} already invited: nothing to do. :-)'.format(group)
				print 'Groups done!'
				for member in wantedmembers:
					print '>>{} ({})'.format(member, member.id)
					if member not in currentmembers:
						print '++ Member {} is not invited: Create MemberInvitation!'.format(member)
						mi = MemberInvitation(event_role=eventrole, member=member)
						print '++ MemberInvitation created: '.format(mi)
						try:
							mi.clean_fields()
							mi.save()
							print '++ MemberInvitation saved'
						except:
							print 'ERROR: Could not save MemberInvitation {}'.format(mi)
							return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Could not save MemberInvitation '+mi+'.' }))
					else:
						print '.. Member {} already invited: nothing to do. :-)'.format(member)
				print 'All done!'
			else: #if we don't want the role:
				print 'No role wanted.'
				try: # check if the role exists and must be removed
					eventrole = EventRole.objects.get(event__id=event.id,role__id=role.id)
					print 'Removing eventrole: %s' % eventrole
					eventrole.delete()
				except: # No role wanted. No role exists. All good.
					print 'No role exists. All good.'
			print ' ..... '

		# for current tags:
		#	if tag not in submitted data:
		#		delete eventtag(event=event,tag=tag)
		# for all TagTypes:
		#	for submitted tags:
		#		if tag not currently saved:
		#			create eventtag(event=event,tag=tag)
		print 'Do tags.'
		print TagType.objects.all()

		print 'Iterate over eventtags'
		for tag in event.tags.all():
			try:
				print 'trying'
				tagslist=data['tag_type'][tagtype.id]
				#if tagslist == None:
				#	tagslist=[]
				#else:
				#	tagslist='hi'
				print 'tried'
			except:
				print 'excepting'
				tagslist=[]
				print 'excepted'
			print 'tagslist: '+str(tagslist)
			if str(tag.id) not in tagslist:
				print 'tag id '+str(tag.id)+' is not in '+str(data['tag_type'][tag.tag_type.id])
				print 'delete eventtag(event=event,tag='+str(tag)+')'
				try:
					et=EventTag.objects.get(event=event,tag=tag)
				except:
					print 'Could not get EventTag.'
					return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Could not get EventTag.' }))
				try:
					et.delete()
				except:
					print 'Could not delete EventTag.'
					return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Could not delete EventTag '+et+'.' }))
			else:
				print 'tag id '+str(tag.id)+' is in '+str(data['tag_type'][tag.tag_type.id])
				print 'Do nothing...'
		print 'Iterate over tagtypes'
		for tagtype in TagType.objects.all():
			if event.event_type in tagtype.event_type.all():
				print tagtype
				print tagtype.id
				try:
					print 'I am trying'
					tagslist=data['tag_type'][tagtype.id]
					print tagslist
					if tagslist == None:
						tagslist=[]
					print 'I tried'
				except:
					print 'I am excepting'
					tagslist=[]
					print 'I have excepted'
				print 'tagslist: '+str(tagslist)
				for tag_id in tagslist:
					tag=Tag.objects.get(pk=tag_id)
					print tag
					if tag not in event.tags.all():
						print 'tag '+str(tag)+' is not in '+str(event.tags.all())
						print 'create eventtag(event=event,tag='+str(tag)+')'
						try:
							et=EventTag(event=event,tag=tag)
						except:
							print 'Could not create EventTag.'
							return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Could not create EventTag.' }))
						try:
							et.clean_fields()
							et.save()
						except:
							print 'Could not save EventTag.'
							return HttpResponse(json.dumps({ 'type': 'error', 'message': 'Could not save EventTag '+et+'.' }))
					else:
						print 'tag '+str(tag)+' is already in '+str(event.tags.all())
						print 'Nothing to do...'
			else:
				print 'tagtype '+str(tagtype)+' is not valid for this event'

		return HttpResponse(json.dumps({ 'type': 'success', 'event_id': event.id }))
