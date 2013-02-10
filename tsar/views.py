# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from events.models import Event

from django.db.models import Q
import datetime

now = datetime.datetime.now()

def my_page(request):
	#recent_events_list = Event.objects.all().order_by('-date_time_begin')[:20]
	recent_events_list = Event.objects.filter(date_time_begin__lte=now).order_by('-date_time_begin')[:20]
	return render_to_response('my_page.html', { 'events_list': recent_events_list })
