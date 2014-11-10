from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from events.models import Event, EventRole, MemberResponse, MemberAttendance
from datetime import datetime
import simplejson as json
from django.views.decorators.csrf import csrf_exempt


def hello(request):
	events_list = Event.objects.all().order_by('-date_time_begin')[:8]
	role_list = EventRole.objects.filter(event_id__in = [event.id for event in events_list])
	member_response = MemberResponse.objects.filter(event_role_id__in = [role.id for role in role_list])
	member_attendance = MemberAttendance.objects.filter(event_role_id__in = [role.id for role in role_list])

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

	return render_to_response('checkin/checkin_index.html', { 'events_list': events_list, 'role_list': role_list, 'member_responses': member_response, 'member_attendance': member_attendance, 'member_response_attendance': listinn})

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
	print 'Checkin in progress'
	if request.is_ajax():
	#Start with gather the information from the request.
		action = request.POST['action']
		member_id = request.POST['member_id']
		event_id = request.POST['event_id']
		role_id = request.POST['role_id']
		event_role_id = request.POST['event_role_id']

		event_role = get_object_or_404(EventRole, id=event_role_id)
		print event_role
		#member = User.objects.get(id=2)
		#print member

		if action == 'attend':
			act = 'Y'
			try:
				ma = MemberAttendance.objects.get(event_role_id=event_role_id, member_id=member_id)
				print '>> MemberAttendance {} found'.format(ma)
				ma.response=act
			except Exception as e:
				ma = MemberAttendance(event_role_id=event_role_id, member_id=member_id, attendance=act,time_checkin = datetime.now())
				print '>> No MemberAttendance found. Creating a new one: {}'.format(ma)
				print e
				try:
					ma.clean_fields()
					ma.save()
					print '>> SAVED'
				except Exception as e:
					print '>> FAILED'
					print e
					return HttpResponse('Failed: could not save member response')
		elif action == 'checkout':
			try:
				ma = MemberAttendance.objects.get(event_role_id=event_role_id, member_id=member_id,)
				ma.time_checkout= datetime.now()
				ma.save()
			except Exception as e:
				print act
		

		

	#print event_role
	data = {
		'action_r': action,
		}
	jsondata = json.dumps(data)
	return HttpResponse(json.dumps(data))