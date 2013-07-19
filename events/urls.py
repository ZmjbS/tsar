from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from events.models import Event

urlpatterns = patterns('',
	url(r'^$', 'events.views.list_events', name='events'),
	#url(r'^(?P<pk>\d+)/$',
	#	DetailView.as_view(
	#		model=Event,template_name='events/event_page.html')
	#	),
	url(r'^(?P<pk>\d+)/$','events.views.display_event', name='events'),
	url(r'^(?P<pk>\d+)/svara$','events.views.event_response', name='events'),
	url(r'^svara$','events.views.event_response', name='events'),
	#url(r'^(?P<pk>\d+)/breyta',
	#	DetailView.as_view(
	#		model=Event,template_name='events/create_event.html')
	#	),
	url(r'^nyskraning/$', 'events.views.display_or_save_event_form', name='events'),
	url(r'^nyskraning/vista$', 'events.views.save_event', name='events'),
)
