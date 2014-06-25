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
		negative_response = False

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
			else:
				negative_response = True

		# Now lets put all this in a dictionary and add it to the list:
		events_dictionaries_list.append({
			'id': event.id,
			'event': event,
			'invitedroles_dictionaries_list': invitedroles_dictionaries_list,
			#'responded_roles': event.responded_roles(member),
			'positive_response': positive_response,
			'negative_response': negative_response,
			#'unanswered_response': unanswered_response,
			#'eventroles': eventroles_dictionaries_list,
		})
	return events_dictionaries_list

from django.contrib.auth.decorators import login_required
@login_required
def my_page(request):
	member = request.user.member

	event_list_length = 20

	# Retrieve a list of upcoming events and place them in a dictionary
	all_events_list = Event.objects.filter(date_time_begin__gte=now).order_by('date_time_begin')[:event_list_length]

	# Retrieve a list of upcoming events for the currently logged in user and place them in a dictionary
	my_events_list = Event.objects.filter(date_time_begin__gte=now).filter(Q(eventrole__invited_positions=request.user.member.position)|Q(eventrole__invited_groups__members=request.user.member)|Q(eventrole__invited_members=request.user.member)|Q(eventrole__is_open=True)).distinct().order_by('date_time_begin')[:event_list_length]
	print my_events_list.count()

	#tmpset = set(all_events_dictionaries_list)# my_events_dictionaries_list)
	union_events_list = list(set(list(all_events_list) + list(my_events_list)))
	union_events_dictionaries_list = member_events_dictionaries_list(member, union_events_list)
	union_events_dictionaries_list = sorted(union_events_dictionaries_list, key=lambda k: k['event'].date_time_begin)

	return render_to_response('my_page.html', {
		'events_dictionaries_list': union_events_dictionaries_list,
		#'my_events_dictionaries_list': my_events_dictionaries_list,
#		'hssr_entries': hssr_entries,
#		'sl_entries': sl_entries,
		'user': request.user,
		'event_list_length': event_list_length,
	})

def news(request):
	print 'doing the news'
	import feedparser
	import locale
	import simplejson as json

	entries = feedparser.parse(request.GET['url']).entries[0:int(request.GET['num'])]
	locale.setlocale(locale.LC_TIME, 'is_IS.UTF-8')
	for entry in entries:
		entry['published'] = date.fromtimestamp(mktime(entry.published_parsed)).isoformat()
		entry['published_parsed'] = date.fromtimestamp(mktime(entry.published_parsed)).strftime('%d. %B %Y.')

	dthandler = lambda obj: (
		obj.isoformat()
		if isinstance(obj, datetime.datetime)
		or isinstance(obj, datetime.date)
		else None)

	response = json.dumps(entries, default=dthandler)
	return HttpResponse(response, mimetype='application/javascript')
