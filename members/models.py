from django.db import models
from django.contrib.auth.models import *
from django.contrib.localflavor.is_.forms import ISIdNumberField, ISPhoneNumberField

class Position(models.Model):
	title = models.CharField(max_length=32)

	def __unicode__(self):
		return self.title

class Member(models.Model):
	user = models.OneToOneField(User)
	member_id = models.IntegerField()
	#id = models.ISIdNumberField()
#	POSITION_CHOICES = (
#		(u'OC', u'On call'),
#		(u'IT', u'In training'),
#		(u'NC', u'Off call'),
#		(u'QT', u'Quit'),
#	#TODO: Do we maybe want to make this editable by giving it a class of its own?
#	)
#	position = models.CharField(max_length=2, choices=POSITION_CHOICES)
	position = models.ForeignKey(Position, default=Position.objects.filter(id=1))
	# TODO: Probably drop this?
	#BLOOD_TYPE_CHOICES = (
	#	(u'AP', u'A RhD pos'),
	#	(u'AN', u'A RhD neg'),
	#	(u'BP', u'B RhD pos'),
	#	(u'BN', u'B RhD neg'),
	#	(u'CP', u'AB RhD pos'),
	#	(u'CN', u'AB RhD neg'),
	#	(u'OP', u'O RhD pos'),
	#	(u'ON', u'O RhD neg'),
	#)
	#blood_type = models.CharField(max_length=2, choices=BLOOD_TYPE_CHOICES, blank=True)
	#ForeignKey-ed in: Phone, Email
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
