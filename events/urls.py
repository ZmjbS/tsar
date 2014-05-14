from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from events.models import Event

urlpatterns = patterns('events.views',
	url(r'^$', 'list_events', name='events'),
	#url(r'^(?P<pk>\d+)/$',
	#	DetailView.as_view(
	#		model=Event,template_name='events/event_page.html')
	#	),
	url(r'^(?P<pk>\d+)/$','display_event', name='events'),
	url(r'^(?P<pk>\d+)/svara$','event_response', name='events'),
	url(r'^svara$','event_response', name='events'),
	#url(r'^(?P<pk>\d+)/breyta',
	#	DetailView.as_view(
	#		model=Event,template_name='events/create_event.html')
	#	),
	url(r'^nyskraning/$', 'display_event_form', name='events'),
	url(r'^nyskraning/vista$', 'save_event', name='events'),
)
