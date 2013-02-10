from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from groups.models import Group

urlpatterns = patterns('groups.views',
	url(r'^$',
		ListView.as_view(
			queryset=Group.objects.order_by('title'),
			context_object_name='group_list',
			template_name='groups/groups_index.html')),
#	url(r'^(?P<slug>\w+)/$',
#		DetailView.as_view(
#			model=Group,
#			template_name='groups/group_page.html')),
	url(r'^(?P<slug>[\w-]+)/$', 'group_page'),
	
)
