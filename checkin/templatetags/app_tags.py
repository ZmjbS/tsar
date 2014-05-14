from django import template
register = template.Library()

@register.filter
def attending(obj, member):
	
	blabla = obj.member_id.get_attending(member)
	print blabla

	return 'N'