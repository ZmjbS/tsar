from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from events.models import Event

urlpatterns = patterns('',
	url(r'^$',
		'events.views.list_events', name='events'),
		#ListView.as_view(
		#	queryset=Event.objects.order_by('-date_time_begin')[:20],
		#	context_object_name='latest_event_list',
		#	template_name='events/events_index.html')),
	#url(r'^skra/$', 'events.views.save_event', name='events'),
	#url(r'^skra/$', 'events.views.create_event', name='events'),
	#url(r'^skra/$', 'events.views.display_event_form', name='events'),
	#url(r'^nyskraning/$', 'events.views.display_event_form', name='events'),
	url(r'^nyskraning/$', 'events.views.display_or_save_event_form', name='events'),
	url(r'^(?P<pk>\d+)/$',
		DetailView.as_view(
			model=Event,
			template_name='events/event_page.html')),
)
