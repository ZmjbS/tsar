# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from events.models import Event

from django.db.models import Q
import datetime

from datetime import date
from time import mktime


now = datetime.datetime.now()

#@login_required
def my_page(request):
	if not request.user.is_authenticated():
		request.user = User.objects.get(id=2)

	# Retrieve a list of upcoming events
	recent_events_list = Event.objects.filter(date_time_begin__gte=now).order_by('date_time_begin')[:20]
	# Retrieve a list of upcoming events for the currently logged in user
	my_events_list = Event.objects.filter(date_time_begin__gte=now).filter(Q(eventrole__invited_groups__members=request.user.member)|Q(eventrole__invited_members=request.user.member)).distinct().order_by('date_time_begin')[:20]
	print my_events_list
	print 'xxx'
	for event in recent_events_list:
		print event
		print event.invited_roles(request.user.member)
	#print recent_events_list
	invited = {}
	#for counter, event in enumerate(recent_events_list):
	#	invited[event] = False
	#	for eventrole in event.eventrole_set.all():
	#		if request.user.member in eventrole.invited_members.all():
	#			print 'invited'
	#			#invited.append(True)
	#			invited[event] = True
	#		else:
	#			print counter
	#			#invited.append(False)
	#		for group in eventrole.invited_groups.all():
	#			if request.user.member in group.members.all():
	#				print 'invited'
	#				invited[event] = True

	import feedparser
	# Landsbjörg
	sl_entries = feedparser.parse('http://landsbjorg.is/Rss.aspx?CatID=466').entries[0:5]
	for entry in sl_entries:
		entry['published'] = date.fromtimestamp(mktime(entry.published_parsed))
	# HSSR
	hssr_entries = feedparser.parse('http://hssr.is/?feed=rss2').entries[0:5]
	for entry in hssr_entries:
		entry['published'] = date.fromtimestamp(mktime(entry.published_parsed))
	return render_to_response('my_page.html', { 'events_list': recent_events_list, 'invited': invited, 'hssr_entries': hssr_entries, 'sl_entries': sl_entries, 'user': request.user, })
