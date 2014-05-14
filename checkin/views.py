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
	for event in events_list:
		print event
		eventrole_list = []
		for eventrole in role_list:
			if eventrole.event_id == event.id:
				#print 'Yes'
				member_response_list = []
				member_attendance_list = []
				for response in member_response:
	#				print response.event_role_id
					if eventrole.id == response.event_role_id:
						print 'Yup'
	#			member_response_list.append({
	#				'member_id': 
	#				})

	return render_to_response('checkin/checkin_index.html', { 'events_list': events_list, 'role_list': role_list, 'member_response': member_response, 'member_attendance': member_attendance})




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
		elif action == 'absent':
			act = 'N'
		print act
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

	#print event_role
	data = {
		'action_r': action,
		}
	jsondata = json.dumps(data)
	return HttpResponse(json.dumps(data))