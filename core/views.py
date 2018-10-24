from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import *
from core.tasks import execute_testcases,add
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
2
def submit(request,test,problem):
	
	if request.method == 'POST' and request.FILES:
		source = request.FILES['source_code']
		problem_status = get_object_or_404(ProblemStatus,pk = problem,user = request.user)
		submission = Submission.objects.create(problem_status=problem_status , code = source)
		submission.save()
		
		job = execute_testcases.delay(submission.code.name, submission.id, problem)
		# job = add.delay(10)
		print (job)
		# return JsonResponse({'job' : 's' })
		# print ( testcase_path )
		
		# microservice and celery
		return HttpResponse('passed')
	else:
		return HttpResponse('failed')

# def task_status(request):
# 	task_id  = request.POST['task_id']

# 	pass


def service(request):
	pass

