from django.db import models
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User

#class User(models.Model):

class Category(models.Model):
	category = models.CharField(max_length=40)

class Department(models.Model):
	name = models.CharField(max_length=40)
	code = models.CharField(max_length=5)

class Semester(models.Model):
	name = models.CharField(max_length=40)#2018 1st semester
	code = models.CharField(max_length=40)#2018S

class Subject(models.Model):
	name = models.CharField(max_length=70)
	code = models.CharField(max_length=40)
	category = models.ForeignKey(Category)
	department = models.ForeignKey(Department)
	plan = models.TextField()
	professor = models.CharField(max_length=40)
	class_number = models.IntegerField()
	capacity = models.IntegerField()
	credit = models.CharField(max_length=40)
	semester = models.ForeignKey(Semester)
	def dict(self):
		return {}

	@property
	def return_credit(self):
		return credit[4]

	@property
	def return_hundred(self):
		return code[4]


class Period(models.Model):
	subject = models.ForeignKey(Subject)
	place = models.CharField(max_length=70)
	start = models.TimeField()
	end = models.TimeField()
	mon = models.BooleanField()
	tue = models.BooleanField()
	wed = models.BooleanField()
	thr = models.BooleanField()
	fri = models.BooleanField()
	def to_dict(self):
		return {}

class Alias(models.Model):
	original = models.ForeignKey(Subject)
	nickname = models.CharField(max_length=70)

class Timetable(models.Model):
	user = models.ForeignKey(User)
	semester = models.ForeignKey(Semester)
	subjects = models.ManyToManyField(Subject)
	def dict(self):
		return {}
