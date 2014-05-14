from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'tsar.views.home', name='home'),
	url(r'^$', 'tsar.views.my_page', name='home'),
	url(r'^hopur/', include('groups.urls')),
	url(r'^felagi/', include('members.urls')),
	url(r'^vidburdur/', include('events.urls')),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
	url(r'^checkin/', include('checkin.urls')),
	url(r'^checkin/$', include('checkin.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)

from django.conf import settings

if settings.DEBUG:
	urlpatterns += patterns('',
		#(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/martin/devel/tsar/static/' }),
	)

