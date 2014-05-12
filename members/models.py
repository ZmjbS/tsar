from django.db import models
from django.contrib.auth.models import *
from django.contrib.localflavor.is_.forms import ISIdNumberField, ISPhoneNumberField

class Position(models.Model):
	# Members can have various positions such as on-call, in training, etc.

	title = models.CharField(max_length=32)

	def __unicode__(self):
		return self.title

class Member(models.Model):
	# This is an object to augment the Django auth system user.
	#
	# The Member has a one-to-one relation to the User but furthermore has:
	# * a member_id which we want for the Icelandic “kennitala”
	# * a position which describes the member status (on-call, in training, etc.)
	# * an address
	# * a text field for general information
	# Furthermore, the Member object has a one-to-many relationship to:
	# * phone numbers (members.phone)
	# * email addresses (members.phone)
	# and a many-to-many relationship to
	# * Group (groups.group)

	user = models.OneToOneField(User)
	member_id = models.IntegerField()
	position = models.ForeignKey(Position, default=Position.objects.filter(id=1))
	address = models.TextField(blank=True)
	info = models.TextField(blank=True)
	
	def __unicode__(self):
		return self.user.first_name +' '+ self.user.last_name

#	TODO: Currently we're just using the auth model email address for the
#	primary, but we might want to add a way to order (not just mark one) the
#	email addresses.
#
#	def email(self):
#		# Return the first primary email address
#		e = Email.objects.filter(member=self, is_primary=True)
#		try:
#			return e[0]
#		except:
#			return ""

	def phone(self):
		# Return the first primary phone number
		p = Phone.objects.filter(member=self, is_primary=True)
		try:
			return p[0]
		except:
			return ""

class Phone(models.Model):
	member = models.ForeignKey(Member)
	number = models.IntegerField()
	#number = models.ISPhoneNumberField()
	is_primary = models.BooleanField(default=False)
	
	def __unicode__(self):
		return str(self.number)

class Email(models.Model):
	member = models.ForeignKey(Member)
	address = models.EmailField(max_length=254)
	is_primary = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.address
