from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'tsar.views.home', name='home'),
	url(r'^$', 'tsar.views.my_page', name='home'),
	url(r'^news/$', 'tsar.views.news', name='news'),

	url(r'^hopur/', include('groups.urls')),
	url(r'^felagi/', include('members.urls')),
	url(r'^vidburdur/', include('events.urls')),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
	url(r'^utskra/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/'}),
	url(r'^checkin/', include('checkin.urls')),
	url(r'^checkin/$', include('checkin.urls')),

	#urls for password reset
	url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
	url(r'^resetpassword/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
	url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

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

