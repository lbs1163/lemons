from django.db import models
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User

#class User(models.Model):

class Category(models.Model):
	category = models.CharField()

class Department(models.Model):
	name = models.CharField()
	code = models.CharField(max_length=5)

class Semester(models.Model):
	name = models.CharField()#2018 1st semester
	code = models.CharField()#2018S

class Subject(models.Model):
	name = models.CharField()
	code = models.CharField()
	category = models.ForeignKey(Category)
	department = models.ForeignKey(Department)
	plan = models.TextField()
	professor = models.CharField()
	class_number = models.IntegerField()
	capacity = models.IntegerField()
	credit = models.CharField()
	semester = models.ForeignKey(Semester)

	def dict(self):
		return {}

class Period(models.Model):
	subject = models.ForeignKey(Subject)
	place = models.CharField()
	start = models.TimeField()
	end = models.TimeField()
	mon = models.BooleanField()
	tue = models.BooleanField()
	wed = models.BooleanField()
	thr = models.BooleanField()
	fri = models.BooleanField()

class Alias(models.Model):
	original = models.ForeignKey(Subject)
	nickname = models.CharField()

class Timetable(models.Model):
	user = models.ForeignKey(User)
	semester = models.ForeignKey(Semester)
	subjects = models.ManyToManyField(Subject)

	# 시간표를 json으로 바꿈
	def dict(self):
		return {}