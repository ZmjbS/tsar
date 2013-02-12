from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from events.models import Event

urlpatterns = patterns('',
	url(r'^$', 'events.views.list_events', name='events'),
	url(r'^(?P<pk>\d+)/$',
		DetailView.as_view(
			model=Event,
			template_name='events/event_page.html')),
	url(r'^nyskraning/$', 'events.views.display_or_save_event_form', name='events'),
	url(r'^nyskraning/test$', 'events.views.test_save', name='events'),
)
