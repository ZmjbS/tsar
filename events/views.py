# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from members.models import Member
from groups.models import Group
from events.models import Role, EventType, Event, EventCreation, EventRoleForm
from django.http import HttpResponseRedirect, HttpResponse

from django.utils import timezone
import datetime
from dateutil import parser

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
	if request.method == 'POST':
		event_role_form = EventRoleForm(request.POST)
		if (form.is_valid()):
			form.save()
		return HttpResponse(json.dumps({ 'form': form, 'event_role_form': event_role_form, 'event_types': event_types, 'event_roles': event_roles, 'members': members, 'groups': groups, }))
	else:
		return render(request, 'events/create_event.html', { 'form': form, 'event_types': event_types, 'event_roles': event_roles, 'members': members, 'groups': groups, })

from django.views.decorators.csrf import csrf_exempt
# TODO: Read up on CSRF <https://docs.djangoproject.com/en/dev/ref/contrib/csrf/>
@csrf_exempt
def test_save(request):
	if request.is_ajax():
		t = request.POST['t']
		d = request.POST['d']
		dtb = timezone.make_aware(parser.parse(request.POST['dtb']),timezone.get_default_timezone())
		dte = timezone.make_aware(parser.parse(request.POST['dte']),timezone.get_default_timezone())
		et_id = request.POST['et']
		try:
			event = Event(title=t, description=d, date_time_begin=dtb, date_time_end=dte, event_type_id=3)
			event.clean_fields()
			#event.save()
		except:
			return HttpResponse("Hello, world. Could not create event.")
		#return HttpResponse("Request is ajax. with Title: "+t+", Description: "+d+", Start: "+dtb.isoformat()+", End: "+dte.isoformat()+" and Type: "+et_id)
		notice = "string"
		return HttpResponse(string)
	else:
		return HttpResponse("Hello, world. Not AJAX request.")
