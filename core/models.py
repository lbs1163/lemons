from django.db import models
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToManyField, ForeignKey

class User(models.Model):
	pass

class Category(models.Model):
	category = models.CharField(max_length=40)
	def to_dict(self):
		result = {}
		result['category'] = self.category
		return result

class Department(models.Model):
	name = models.CharField(max_length=40)
	code = models.CharField(max_length=5)
	def to_dict(self):
		result = {}
		result['name'] = self.name
		result['code'] = self.code
		return result

class Semester(models.Model):
	name = models.CharField(max_length=40)#2018 1st semester
	code = models.CharField(max_length=40)#2018S
	def to_dict(self):
		result = {}
		result['name'] = self.name
		result['code'] = self.code
		return result

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
	def to_dict(self):
		result = {}
		result['name'] = self.name
		result['code'] = self.code
		result['category'] = self.category.to_dict()
		result['department'] = self.department.to_dict()
		result['plan'] = self.plan
		result['professor'] = self.professor
		result['class_number'] = self.class_number
		result['capacity'] = self.capacity
		result['credit'] = self.credit
		result['semester'] = self.semester.to_dict()
		return result

class Period(models.Model):
	subject = models.ForeignKey(Subject)
	place = models.CharField(max_length=70)
	start = models.TimeField()
	end = models.TimeField()
	mon = models.BooleanField()
	tue = models.BooleanField()
	wed = models.BooleanField()
	thu = models.BooleanField()
	fri = models.BooleanField()
	def to_dict(self):
		result = {}
		result['subject'] = self.subject.to_dict()
		result['place'] = self.place
		result['start'] = self.start
		result['end'] = self.end
		result['mon'] = self.mon
		result['tue'] = self.tue
		result['wed'] = self.wed
		result['thu'] = self.thu
		result['fri'] = self.fri
		return result

class Alias(models.Model):
	original = models.ForeignKey(Subject)
	nickname = models.CharField(max_length=70)

class Timetable(models.Model):
	user = models.ForeignKey(User)
	semester = models.ForeignKey(Semester)
	subjects = models.ManyToManyField(Subject)
	def to_dict(self):
		result = {}
		result['user'] = self.user
		result['semester'] = self.semester.to_dict()

		for f in self._meta.many_to_many:
			if self.pk is None:
				result[f.name] = []
			else:
				index_list = list(f.value_from_object(self).values_list('pk', flat=True))
				result_temp = []
				for item in index_list:
					result_temp.append(Subject.objects.filter(id=item)[0].to_dict())
				result[f.name] = result_temp
		return result