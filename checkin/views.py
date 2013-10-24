from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from events.models import Event, EventRole, MemberResponse, MemberAttendance
import simplejson as json
from django.views.decorators.csrf import csrf_exempt


def hello(request):
	events_list = Event.objects.all().order_by('-date_time_begin')
	role_list = EventRole.objects.all()
	member_response = MemberResponse.objects.all()
	member_attendance = MemberAttendance.objects.all()
	return render_to_response('checkin/checkin_index.html', { 'events_list': events_list, 'role_list': role_list, 'member_response': member_response, 'member_attendance': member_attendance})

@csrf_exempt
def event_checkin(request):
	print 'Checkin in progress'
	#Start with gather the information from the request.
	action = request.POST['action']
	#eventrole_id = request.POST['eventrole_id']
	#member_id = request.POST['member_id']
	#event_id = request.POST['event_id']
	role_id = request.POST['role_id']


	if action == 'attend':
			act = 'Y'
	print action
	#event_role = get_object_or_404(EventRole, id=eventrole_id)

	#print event_role
	data = {
		'action_r': action,
		}
	return HttpResponse(json.dumps(data))