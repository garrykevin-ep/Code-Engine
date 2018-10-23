from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Test(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class TestStatus(models.Model):
	test = models.ForeignKey(Test, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	#status


class Problem(models.Model):
	test = models.ForeignKey(Test, on_delete = models.CASCADE)
	statement = models.TextField()
	
	def __str__(self):
		return self.test.name


class TestCase(models.Model):
	problem = models.ForeignKey(Problem,on_delete = models.CASCADE)
	testcase = models.FileField(upload_to="testcase")
	output = models.FileField(upload_to="output")

class ProblemStatus(models.Model):
	problem = models.ForeignKey(Problem,on_delete = models.CASCADE)
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	#status =>  accepted , wrong answer , not_attempted
	#count of submission
	#status


class Submission(models.Model):
	problem_status = models.ForeignKey(ProblemStatus,on_delete=models.CASCADE)
	code = models.FileField(upload_to='code/')
	# time
	#status => running , failed  , accepted , wrong answer

class SubmissionTestcaseStatus(models.Model):
	submission = models.ForeignKey(Submission,on_delete = models.CASCADE)
	testcase  = models.ForeignKey(TestCase,on_delete = models.CASCADE)
	#status correct,wrong