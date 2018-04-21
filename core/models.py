from django.db import models
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User

#class User(models.Model):

class Category(models.Model):
	category = models.CharField(max_length=40)
	def __str__(self):
		return self.category

class Department(models.Model):
	name = models.CharField(max_length=40)
	code = models.CharField(max_length=5)
	def __str__(self):
		return self.name

class Semester(models.Model):
	name = models.CharField(max_length=40)#2018 1st semester
	code = models.CharField(max_length=40)#2018S
	def __str__(self):
		return self.name

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
	def __str__(self):
		return self.name
	def dict(self):
		return {}


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
	def __str__(self):
		return self.subject+" "+self.place
	def to_dict(self):
		return {}

class Alias(models.Model):
	original = models.ForeignKey(Subject)
	nickname = models.CharField(max_length=70)
	def __str__(self):
		return self.nickname+"="+self.original

class Timetable(models.Model):
	user = models.ForeignKey(User)
	semester = models.ForeignKey(Semester)
	subjects = models.ManyToManyField(Subject)
	def __str__(self):
		return self.user+" "+self.semester
	def dict(self):
		return {}
