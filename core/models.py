from django.db import models
from django.utils import timezone

#class User(models.Model):

class Category(models.Model):
	category = models.Charfield()

class Department(models.Model):
	name = models.CharField()
	code = models.CharField(max_length=5)

class Semester(models.Model):
	name = models.CharField()#2018 1st semester
	code = models.Charfield()#2018S

class Subject(models.Model):
	name = models.CharField()
	code = models.CharField()
	category = models.ForeignKey(Category)
	department = models.ForeignKey(Department)
	plan = models.textField()
	professor = models.CharField()
	class_number = models.integerField()
	capacity = models.integerField()
	credit = models.CharField()
	semester = models.ForeignKey(Semester)

	@property
	def return_credit(self):
		return credit[4]

	@property
	def return_hundred(self):
		return code[4]


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