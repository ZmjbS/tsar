from django.conf.urls import patterns, include, url
from events.models import Event

urlpatterns = patterns('',
	url(r'^$', 'checkin.views.checkin'),
	url(r'^add$','checkin.views.event_checkin', name='checkin'),
	url(r'^edit/(?P<event_id>\d+)/$', 'checkin.views.edit_event'),
	url(r'^edit/checkin$','checkin.views.checkin_edit'),
)
