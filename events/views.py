# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from members.models import Member
from groups.models import Group
from events.models import Role, Event, EventCreation, EventRoleForm
from django.http import HttpResponseRedirect

#from django.utils import timezone
import datetime

now = datetime.datetime.now()

def list_events(request):
	recent_events_list = Event.objects.filter(date_time_begin__lte=now).order_by('-date_time_begin')[:20]
	coming_events_list = Event.objects.filter(date_time_begin__gte=now).order_by('date_time_begin')[:20]
	return render_to_response('events/events_index.html', { 'recent_events_list': recent_events_list, 'coming_events_list': coming_events_list })

def display_or_save_event_form(request):
	event_roles = Role.objects.all()
	members = Member.objects.all()
	groups = Group.objects.all()
	form = EventCreation(request.POST)
	if request.method == 'POST':
		event_role_form = EventRoleForm(request.POST)
		if (form.is_valid()):
			form.save()
		return HttpResponse(json.dumps({ 'form': form, 'event_role_form': event_role_form, 'event_roles': event_roles, 'members': members, 'groups': groups, }))
	else:
		return render(request, 'events/create_event.html', { 'form': form, 'event_roles': event_roles, 'members': members, 'groups': groups, })

def display_event_form(request):
	form = EventCreation(request.POST)
	event_roles = Role.objects.all()
	members = Member.objects.all()
	groups = Group.objects.all()
	if request.POST == 'invite':
		event_role_form = EventRoleForm(request.POST)
		return render(request, 'events/create_event.html', { 'form': form, 'event_role_form': event_role_form, 'event_roles': event_roles, 'members': members, 'groups': groups, })
	else:
		return render(request, 'events/create_event.html', { 'form': form, 'event_roles': event_roles, 'members': members, 'groups': groups, })

## Receive a POST request from JavaScript and create (or update) the event.
#def save_event(request):
#	if request.method == 'POST':
#		if request.POST == 'save':
#			e = EventCreation(request.POST)
#			if e.is_valid():
#				e.save()
#	#			return display_event_form(request)
#				#return render(request, 'events/create_event.html', { 'event': e, })
#			else:
#				return display_event_form(request)
#		if request.POST == 'event-invite-button':
#			e = EventCreation(request.POST)
#			if e.is_valid():
#				e.save()
#	#			return display_event_form(request)
#	else:
#		return render_to_response('Not POST request')
#
## Receive a POST request from JavaScript and add or update roles to an event.
#def save_role(request):
#	if request.method == 'POST':
#		e = Event.objects(id=request.POST.event_id)
#		e_r = EventRoleForm(request.POST)
#		if e_r.is_valid():
#			e_r.save()
#			return render(request, 'events/create_event.html', { 'event': e, 'event_role': e_r, } )
#	else:
#		return render('Not POST')

# Receive a POST request from JavaScript and add or update tags to an event.
#def save_tag(request):

#def create_event(request):
#	if request.method == 'POST':
#		form = EventCreation(request.POST)
#		#e = Event(title="annar titill", description="Lýsingin", date_time_begin=timezone.now(), date_time_end=timezone.now(), event_type_id="1")
#		#e.save()
#		# Process data in form.cleaned_data
#		form.date_time_begin = timezone.now()
#		form.date_time_end= timezone.now()
#		form.event_type_id="1"
#		if form.is_valid():
#			form.save()
#			return HttpResponseRedirect('')
#	else:
#		form = EventCreation(request.POST)
#
#	return render(request, 'events/create_event.html', { 'form': form, })
