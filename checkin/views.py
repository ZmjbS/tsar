# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from events.models import Event, EventRole, EventQuickCreation, MemberResponse, MemberAttendance, MemberInvitation, GroupInvitation, Member
from members.models import Member, Position
from datetime import datetime, timedelta
from django.utils import formats
import json
from django.views.decorators.csrf import csrf_exempt


def checkin(request):
	events_list = Event.objects.filter(date_time_begin__lt=datetime.now()).order_by('-date_time_begin')[:8]
	role_list = EventRole.objects.filter(event_id__in = [event.id for event in events_list])
	member_response = MemberResponse.objects.filter(event_role_id__in = [role.id for role in role_list])
	member_attendance = MemberAttendance.objects.filter(event_role_id__in = [role.id for role in role_list])
	form = EventQuickCreation(request.POST)
	members = Member.objects.select_related().all()

	listinn = []
	for response in member_response:
		attendance = getAttendance(member_attendance, response.event_role_id, response.member_id)
		time_checkin = getTimeCheckin(member_attendance, response.event_role_id, response.member_id)
		time_checkout = getTimeCheckout(member_attendance, response.event_role_id, response.member_id)
		listinn.append({
			'event_role_id': response.event_role_id,
			'member_id': response.member_id,
			'response' : response.response,
			'attendance' : attendance,
			'time_checkin' : time_checkin,
			'time_checkout' : time_checkout,
			})

	return render_to_response('checkin/checkin_index.html', { 'events_list': events_list, 'role_list': role_list, 'member_responses': member_response, 'member_attendance': member_attendance, 'member_response_attendance': listinn, 'form': form, 'members': members})

def edit_event(request,event_id):
	event_description = Event.objects.get(id= event_id)
	eventrole_list = EventRole.objects.filter(event = event_id)
	invitations_responses = MemberInvitation.objects.filter(event_role_id__in = [role.id for role in eventrole_list]).only('event_role', 'member')
	responses = MemberResponse.objects.filter(event_role_id__in = [role.id for role in eventrole_list], response = 'Y').only('event_role', 'member')
	attendances = MemberAttendance.objects.filter(event_role_id__in = [role.id for role in eventrole_list])

	members = []
	for member in Member.objects.select_related(depth=0).all():
		members.append(member)
	#Good idea to sort the list of members by name:
	members.sort(key=lambda member: (member.user.first_name, member.user.last_name))


	roledata=[]
	event = get_object_or_404(Event.objects.select_related('eventtype', 'eventrole_set', 'tags'), id=event_id)
	for eventrole in EventRole.objects.select_related('memberresponse_set','invited_positions','invited_groups','invited_members').filter(event=event):
		memberss=[]
		for memberresponse in MemberResponse.objects.filter(event_role=eventrole).select_related('event_role','member__user__id'):
			memberss.append(memberresponse.member)
		for member in Member.objects.select_related('user').filter(position__eventrole=eventrole):
			if member not in memberss:
				memberss.append(member)
		for member in Member.objects.select_related('user').filter(group__groupinvitation__event_role=eventrole):
			if member not in memberss:
				memberss.append(member)
		for member in Member.objects.select_related('user').filter(memberinvitation__event_role=eventrole):
			if member not in memberss:
				memberss.append(member)
		roledata.append({
			'id': eventrole.role.id,
			'title': eventrole.role.title,
			'eventrole': eventrole,
			'invited_members':memberss,
			})

	return render_to_response('checkin/checkin_edit.html',{'event_id': event_id, 'event': event_description, 'role_list': eventrole_list, 'invitations_responses': invitations_responses, 'attendances': attendances, 'members': members,'roledata':roledata})

def getAttendance(attendance_list, event_role_id, member_id):
	found = False
	for attendance in attendance_list:
		if attendance.member_id == member_id and attendance.event_role_id == event_role_id:
			found = True
	return found

def getTimeCheckin(attendance_list, event_role_id, member_id):
	time_checkins = False
	for attendance in attendance_list:
		if attendance.member_id == member_id and attendance.event_role_id == event_role_id:
			time_checkins = attendance.time_checkin
	return time_checkins

def getTimeCheckout(attendance_list, event_role_id, member_id):
	time_checkout = False
	for attendance in attendance_list:
		if attendance.member_id == member_id and attendance.event_role_id == event_role_id:
			time_checkout=attendance.time_checkout
	return time_checkout

@csrf_exempt
def event_checkin(request):
	print('Checkin in progress')
	if request.is_ajax():
	#Start with gather the information from the request.
		action = request.POST['action']
		member_id = request.POST['member_id']
		event_id = request.POST['event_id']
		role_id = request.POST['role_id']
		event_role_id = request.POST['event_role_id']

		event_role = get_object_or_404(EventRole, id=event_role_id)
		print(event_role)
		#member = User.objects.get(id=2)
		#print(member)

		if action == 'attend':
			act = 'Y'
			try:
				ma = MemberAttendance.objects.get(event_role_id=event_role_id, member_id=member_id)
				print('>> MemberAttendance {} found'.format(ma))
				ma.response=act
			except Exception as e:
				ma = MemberAttendance(event_role_id=event_role_id, member_id=member_id, attendance=act,time_checkin = datetime.now())
				print('>> No MemberAttendance found. Creating a new one: {}'.format(ma))
				print(e)
				try:
					ma.clean_fields()
					ma.save()
					print('>> SAVED')
				except Exception as e:
					print('>> FAILED')
					print(e)
					return HttpResponse('Failed: could not save member response')
		elif action == 'checkout':
			try:
				ma = MemberAttendance.objects.get(event_role_id=event_role_id, member_id=member_id,)
				ma.time_checkout= datetime.now()
				ma.save()
			except Exception as e:
				print(act)
		
		attendance = MemberAttendance.objects.get(event_role_id=event_role_id, member_id=member_id)
		time_checkin = attendance.time_checkin
		time_checkout = attendance.time_checkout
		print(time_checkin)
		print(time_checkout)

		# Tooltip for times configured
		if time_checkout != None:
			tooltip = "INN: "+str(formats.date_format(time_checkin, 'TIME_FORMAT'))+"\n  ÚT: "+str(formats.date_format(time_checkout, 'TIME_FORMAT'))
		else :
			tooltip = "INN: "+str(formats.date_format(time_checkin, 'TIME_FORMAT'))
		print(tooltip)

		#print(time_inn)

		

	#print(event_role)
	data = {
		'action_r': action,
		'tooltip': tooltip
		}
	jsondata = json.dumps(data)
	return HttpResponse(json.dumps(data))

@csrf_exempt
def checkin_edit(request):
	print('Checkin in progress!')
	if request.is_ajax():
		print('Request is AJAX')
		data = request.POST['data']
		event_id = request.POST['event_id']
		new_data = json.loads(data)
		# Lets find out if the member already has an attendance logged
		for row in new_data:
			print(row[u'role_id'])
			print(row[u'member'])
			try:
				ma = MemberAttendance.objects.get(event_role_id=row[u'role_id'], member_id=row[u'member'])
				print(row[u'id'])
				if "checkin" in row[u'id']:
					if row[u'value'] == "":
						print('Value is empty')
						ma.delete()
						print('DELETED')
					else:
						print('Time to save this checkin time'+row[u'value'])
						ma.time_checkin= row[u'value']
						ma.save()
				elif "checkout" in row[u'id']:
					if row[u'value'] == "":
						print('Value is empty')
						ma.time_checkout = None
						ma.save()
					else:
						print('Time to save this checkout time'+row[u'value'])
						ma.time_checkout= row[u'value']
						ma.save()
			except Exception as e:
				print('>> No MemberAttendance found. Creating a new one: {}')
				ma = MemberAttendance(event_role_id=row[u'role_id'], member_id=row[u'member'], attendance="Y",time_checkin = datetime.now())
				try: 
					mr = MemberResponse.objects.get(event_role_id=row[u'role_id'], member_id=row[u'member'])
				except Exception as e:
					mr = MemberResponse(event_role_id=row[u'role_id'], member_id=row[u'member'], response="Y",time_responded = datetime.now())
				try: 
					mi = MemberInvitation.objects.get(event_role_id=row[u'role_id'], member_id=row[u'member'])
				except Exception as e:
					mi = MemberInvitation(event_role_id=row[u'role_id'], member_id=row[u'member'])
				
				ma.clean_fields()
				mr.clean_fields()
				mi.clean_fields()
				ma.save()
				mr.save()
				mi.save()
		
	else:
		print('Request is not AJAX')


	datab = {
		'action': data
		}
	#jsondata = json.dumps(datab)
	print('After if')
	return HttpResponse(json.dumps(data))