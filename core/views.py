from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import *
from core.tasks import execute_testcases,add
from celery.result import AsyncResult
# Create your views here.

def showproblem(request,test,problem):
	problem = get_object_or_404(Problem,pk=problem,test=test)
	testcases = TestCase.objects.filter(problem=problem)
	context = { 
		'statement' : problem.statement , 
		'test' : problem.test.id ,
		'problem' : problem.id ,
		'testcases' : testcases
		}
	return render(request,'core/showproblem.html',context)

def submit(request,test,problem):
	
	if request.method == 'POST' and request.FILES:
		source = request.FILES['source_code']
		problem_status = get_object_or_404(ProblemStatus,pk = problem,user = request.user)
		submission = Submission.objects.create(problem_status=problem_status , code = source)
		submission.save()
		
		job = execute_testcases.delay(submission.code.name, submission.id, problem)
		task = AsyncResult(job.task_id)
		print (task.result)
		# microservice and celery
		return JsonResponse({'id' : job.task_id})
	else:
		return HttpResponse('failed')

def task_status(request):
	task_id  = request.POST['task_id']
	task = AsyncResult(task_id)
	print (task.result)
	if task.state == 'SUCCESS':
		return JsonResponse(task.result)
	else:
		return JsonResponse(task.result,status=400,safe=False)

# 	pass



