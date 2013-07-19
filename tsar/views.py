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

def member_events_dictionaries_list(member, events_list):
	events_dictionaries_list = []
	for event in events_list:
		invitedroles_dictionaries_list = []
		positive_response = False
		unanswered_response = False

		# Collect some data about each EventRole which the user is invited to.
		for eventrole in event.invited_roles(member):
			# Get the current user's response to this EventRole: 'Y', 'N' or 'U' (No response returns 'U'). 
			response = eventrole.response(member)
			# Place the response with the eventrole in a list:
			invitedroles_dictionaries_list.append({
				'eventrole': eventrole, # EventRole
				'response': response,	# 'Y', 'N' or 'U'
			})

			# Check whether the user has accepted any of the EventRoles or not declined all:
			if response == 'Y':
				positive_response = True
			elif response != 'N':
				unanswered_response = True

		# Now lets put all this in a dictionary and add it to the list:
		events_dictionaries_list.append({
			'id': event.id,
			'event': event,
			'invitedroles_dictionaries_list': invitedroles_dictionaries_list,
			#'responded_roles': event.responded_roles(member),
			'positive_response': positive_response,
			'unanswered_response': unanswered_response,
			#'eventroles': eventroles_dictionaries_list,
		})
	return events_dictionaries_list

#@login_required
def my_page(request):
	# TODO: Remove the hardcoded user once we have anonymous test users!
	if not request.user.is_authenticated():
		request.user = User.objects.get(id=2)
	#request.user = User.objects.get(id=2)
	member = request.user.member

	# Retrieve a list of upcoming events and place them in a dictionary
	all_events_list = Event.objects.filter(date_time_begin__gte=now).order_by('date_time_begin')[:20]
	all_events_dictionaries_list = member_events_dictionaries_list(member, all_events_list)

	# Retrieve a list of upcoming events for the currently logged in user and place them in a dictionary
	my_events_list = Event.objects.filter(date_time_begin__gte=now).filter(Q(eventrole__invited_groups__members=request.user.member)|Q(eventrole__invited_members=request.user.member)).distinct().order_by('date_time_begin')[:20]
	my_events_dictionaries_list = member_events_dictionaries_list(member, my_events_list)

	import pprint
	pprint.pprint(all_events_dictionaries_list)
	#pprint.pprint(my_events_dictionaries_list)

	# Import news from defined news sites:
	import feedparser
	# Landsbjörg
#	sl_entries = feedparser.parse('http://landsbjorg.is/Rss.aspx?CatID=466').entries[0:5]
#	for entry in sl_entries:
#		entry['published'] = date.fromtimestamp(mktime(entry.published_parsed))
#	# HSSR
#	hssr_entries = feedparser.parse('http://hssr.is/?feed=rss2').entries[0:5]
#	for entry in hssr_entries:
#		entry['published'] = date.fromtimestamp(mktime(entry.published_parsed))
	#return render_to_response('my_page.html', { 'events_list': all_events_list, 'invited': invited, 'hssr_entries': hssr_entries, 'sl_entries': sl_entries, 'user': request.user, })
	return render_to_response('my_page.html', {
		'all_events_dictionaries_list': all_events_dictionaries_list,
		'my_events_dictionaries_list': my_events_dictionaries_list,
#		'hssr_entries': hssr_entries,
#		'sl_entries': sl_entries,
		'user': request.user,
	})
