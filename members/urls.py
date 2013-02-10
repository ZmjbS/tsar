from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from members.models import Member

urlpatterns = patterns('members.views',
	url(r'^$',
		ListView.as_view(
			queryset=Member.objects.order_by('user__first_name', 'user__last_name'),
			context_object_name='member_list',
			template_name='members/members_list.html')),
	url(r'^(?P<slug>\w+)/$',
		DetailView.as_view(
			model=Member,
			slug_field = 'user__username',
			template_name='members/member_page.html')),
)
