from django.db import models
from django.contrib.auth.models import User

from django.utils.timezone import now

# Create your models here.

class Thing(models.Model):
	name = models.CharField(max_length=255)
	location = models.CharField(max_length=255, blank=True)
	description = models.TextField(blank=True)
	owner = models.ForeignKey(User)
	
	def __unicode__(self):
		return self.name;

class Metric(models.Model):
	thing = models.ForeignKey(Thing, related_name='metrics')
	name = models.CharField(max_length=255)
	unit = models.CharField(max_length=64, blank=True)
	
	class Meta:
		unique_together = (("name","thing"),)
	
	def __unicode__(self):
		return self.name;
	
	""" Return most recent value for metric """
	@property
	def current_value(self):
		try:
			return Value.objects.filter(metric = self)[:1].get().value
		except Value.DoesNotExist:
			return None
	
	""" set current value by adding a new Value with current timestamp"""
	@current_value.setter
	def current_value(self, value):
		v = Value(metric = self, value = value)
		v.save()
	
	""" Return datetime of last update """
	@property
	def last_update(self):
		try:
			return Value.objects.filter(metric = self)[:1].get().timestamp
		except Value.DoesNotExist:
			return None

class Value(models.Model):
	metric = models.ForeignKey(Metric)
	value = models.FloatField()
	timestamp = models.DateTimeField(default=now)
	
	class Meta:
		ordering = ['-timestamp']
	
