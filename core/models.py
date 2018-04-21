from django.db import models
from django.utils import timezone

#class User(models.Model):

class Category(models.Model):
	category

class Department(models.Model):
	name = models.CharField()
	code = models.CharField(max_length=5)

class Semester(models.Model):
	string = models.CharField()

class Subject(models.Model):
	name = models.CharField()
	code = models.CharField()
	category = models.ForeignKey(Category)
	department = models.ForeignKey(Department)
	plan = models.textField()
	place = models.CharField()
	professor = models.CharField()
	class_number = models.integerField()
	capacity = models.integerField()
	credit = models.CharField()
	semester = models.ForeignKey(Semester)

class Period(models.Model):
	subject = models.ForeignKey(Subject)
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