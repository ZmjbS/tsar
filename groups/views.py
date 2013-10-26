# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from members.models import Member
from groups.models import Group, Membership
from events.models import Event, EventRole, MemberResponse

import datetime

now=datetime.datetime.now()

def index(request):
	all_groups_list = Group.objects.all().order_by('title')
	return render_to_response('groups/groups_index.html', {
		'group_list': all_groups_list,
		'user': request.user,
	})

from django.contrib.auth.decorators import login_required

#@login_required
def group_page(request, slug):
	g = get_object_or_404(Group, slug=slug)
	#import pprint
	#pprint.pprint(g.members.all())
	managers = [ membership.member for membership in Membership.objects.filter(group=g).filter(is_manager=True) ]
	print managers
	om = Member.objects.exclude(membership__group__slug=slug)
	recent_events_list=Event.objects.filter(eventrole__groupinvitation__group__slug=slug).filter(date_time_begin__lte=now).distinct()
	coming_events_list=Event.objects.filter(eventrole__groupinvitation__group__slug=slug).filter(date_time_begin__gte=now).distinct()
	return render_to_response('groups/group_page.html', {
		'group': g,
		'managers': managers,
		'members': om,
		'recent_events_list': recent_events_list,
		'coming_events_list': coming_events_list,
		'user': request.user,
	})

import simplejson as json
def save_group(request):
	if not request.is_ajax():
		return False
	else:
		print request.POST
		data = json.loads(request.POST['data'])
		print data['member']
		# Check whether the group exists:
		try:
			group = get_object_or_404(Group, id=data['group_id'])
		except:
			return HttpResponse('no such group')

		# Iterate over the membership array
		for (member_id,group_status) in enumerate(data['member'][1:]):
			print '>> Member {}: {}'.format(member_id+1,group_status)
			if group_status != None or group_status != 'member':
				# Check whether the member exists:
				try:
					print 'Finding member {}'.format(member_id+1)
					member = get_object_or_404(Member, id=member_id+1)
					print 'member {} found'.format(member)
				except:
					print 'member not found'
					return HttpResponse('no such member')

				# If we need to add the member...
				if group_status == 'add-member':
					print '>>> Add member!'
					try:
						membership = get_object_or_404(Membership, member=member, group=group)
						return HttpResponse('member already exists')
					except:
						print '>> Create membership object!'
						membership = Membership(member=member, group=group)
					try:
						print '>> Clean and save membership object!'
						membership.clean()
						membership.save()
					except:
						return HttpResponse('unable to save membership')

				# If we need to remove the member...
				elif group_status == 'remove-member':
					print '>>> Remove member!'
					try:
						membership = get_object_or_404(Membership, member=member, group=group)
					except:
						print '>> No membership to remove. We\'re done!'
					try:
						membership.delete()
					except:
						return HttpResponse('unable to delete membership')
		# All is done. Return a successful response to the template. :-)
		return HttpResponse(json.dumps({ 'type': 'success' }))

def group_stats(request, slug):
	g = get_object_or_404(Group, slug=slug)

	# Get the last N events (that match cerctain criteria, such as the group is the organiser?)
	# Create an array (dictionary) with members and events.
	# Add a line for total attendance for each member and each event
	# In template:
	# * Create table
	# * make table sortable by attendance
	# * Plot a bar-chart with attendance vs. event
	#import pprint
	#pprint.pprint(g.members.all())

	gm = Member.objects.filter(membership__group__slug=slug)
	recent_events_list=Event.objects.filter(eventrole__groupinvitation__group__slug=slug).filter(date_time_begin__lte=now).distinct()
	events_list = []
	for event in recent_events_list:
		attendees = []
		for eventrole in EventRole.objects.filter(event=event):
			# TODO: We need to change this into an attendance to see who actually attended (check Tóti's part).
			for mr in MemberResponse.objects.filter(event_role=eventrole):# with event.memberresponse.response == 'Y':
				if mr.member in gm and mr.response == 'Y':
					attendees.append(mr.member)
		events_list.append({ 'event': event, 'attendees': attendees})

	# Count the number of times each member has attended:
	members_list = []
	for member in gm:
		attendences = 0
		for event in events_list:
			if member in event['attendees']:
				attendences += 1
		members_list.append({'member': member, 'attendences': attendences})

	print members_list
		#for event in events_list:
			#if member in event['attendees']:
				#members_list.append({ 'member': member, 'attendences': members

	print gm 
	import pprint
	pprint.pprint(events_list)
			
	managers = [ membership.member for membership in Membership.objects.filter(group=g).filter(is_manager=True) ]
	om = Member.objects.exclude(membership__group__slug=slug)
	return render_to_response('groups/group_stats.html', {
		'group': g,
		'group_members': gm,
		'managers': managers,
		'members': om,
		'recent_events_list': recent_events_list,
		'user': request.user,
		'events_list': events_list,
		'members_list': members_list,
	})

