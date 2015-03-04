from django import template
from django.template.defaultfilters import register

register = template.Library()


@register.filter
def get_item(dictionary, key):

	key1 = str(key)

	member, event_role = key1.split()
	member = member.replace("t","")
	event_role = event_role.replace("t","")

	if dictionary.filter(member_id=member, event_role_id=event_role).exists():
		result = dictionary.filter(member_id=member, event_role_id=event_role).values().get()
   	else:
   		result = None
   	return result