# -*- coding: utf-8 -*-
from django.db import models
from members.models import Member
from datetime import datetime

class Group(models.Model):
	title = models.CharField(max_length=64)
	slug = models.SlugField()
	description = models.TextField()
	members = models.ManyToManyField(Member, through='Membership')
	GROUP_TYPE_CHOICES = (
		(u'UH', u'útkallshópur'),
		(u'AH', u'almennur hópur'),
		(u'FL', u'flokkur'),
	)
	group_type = models.CharField(max_length=2, choices=GROUP_TYPE_CHOICES, default='UH')
	#qualifications = models.ManyToManyField(Qualification, through='Qualify')
	
	def __unicode__(self):
		return self.title

class Membership(models.Model):
	member = models.ForeignKey(Member)
	group = models.ForeignKey(Group)
	date_joined = models.DateField(default=datetime.now)
	is_leader = models.BooleanField(default=False)

#class Qualify(models.Model):
#	qualification = models.ForeignKey(Qualification)
#	group = models.ForeignKey(Group)
# TODO: Is a required minimum number really useful?
#	required_minimum_number = models.PositiveSmallIntegerField(default='0')
