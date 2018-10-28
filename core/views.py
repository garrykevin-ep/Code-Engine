from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.conf import  settings
from .models import *
from core.tasks import execute_testcases,add,execute
from celery.result import AsyncResult,GroupResult
from celery import group
from pathlib import Path
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
		testcases = TestCase.objects.filter(problem=problem)
		base_dir = Path(settings.MEDIA_ROOT).resolve()
		source_path = base_dir / submission.code.name
		jobs = []
		test_case_id = []
		for testcase in testcases:
			testcase_path = base_dir / testcase.testcase.name
			output_path = base_dir / 'user_output' /( str(submission.id) + str(testcase.id))
			jobs.append(execute.s(base_dir=str(base_dir), source_path=str(source_path), testcase_path=str(testcase_path), output_path=str(output_path)))
			test_case_id.append(testcase.id)
		
		jobs = group(jobs)

		group_result = jobs.apply_async()
		
		response = {k: str(v) for k,v in zip(test_case_id,group_result.results)}
		
		return JsonResponse(response)
	else:
		return HttpResponse('failed')

def task_status(request):
	response = {}
	check_again = False

	for testcase,task in zip(request.POST.keys(),request.POST.values()):
		result = AsyncResult(task)
		if result.state == 'SUCCESS':
			response[testcase] = result.result
		else:
			check_again = True
	
	if check_again == True:
		return JsonResponse(response,status=400,safe=False)
	else:
		return JsonResponse(response)



