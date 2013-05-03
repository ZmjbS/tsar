# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from events.models import Event

from django.db.models import Q
import datetime

from datetime import date
from time import mktime


now = datetime.datetime.now()

def my_page(request):
	#recent_events_list = Event.objects.all().order_by('-date_time_begin')[:20]
	recent_events_list = Event.objects.filter(date_time_begin__gte=now).order_by('date_time_begin')[:20]
	import feedparser
	# Landsbjörg
	sl_entries = feedparser.parse('http://landsbjorg.is/Rss.aspx?CatID=466').entries[0:5]
	for entry in sl_entries:
		entry['published'] = date.fromtimestamp(mktime(entry.published_parsed))
	# HSSR
	hssr_entries = feedparser.parse('http://hssr.is/?feed=rss2').entries[0:5]
	for entry in hssr_entries:
		entry['published'] = date.fromtimestamp(mktime(entry.published_parsed))
	return render_to_response('my_page.html', { 'events_list': recent_events_list, 'hssr_entries': hssr_entries, 'sl_entries': sl_entries})
