from django.conf.urls import patterns, include, url
from events.models import Event

urlpatterns = patterns('',
	url(r'^$', 'checkin.views.hello'),
	url(r'^add$','checkin.views.event_checkin', name='checkin'),
)
