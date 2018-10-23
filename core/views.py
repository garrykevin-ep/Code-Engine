from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import *
from engine.core import Engine
from django.conf import  settings
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
2
def submit(request,test,problem):
	base_dir = Path(settings.MEDIA_ROOT).resolve()
	if request.method == 'POST' and request.FILES:
		source = request.FILES['source_code']
		problem_status = get_object_or_404(ProblemStatus,pk = problem,user = request.user)
		submission = Submission.objects.create(problem_status=problem_status , code = source)
		submission.save()
		source_path = base_dir / submission.code.name
		testcases = TestCase.objects.filter(problem=problem)
		response = {}
		
		for testcase in testcases:
			testcase_path = base_dir / testcase.testcase.name
			output_path = base_dir / 'user_output' /( str(submission.id) + str(testcase.id))
			engine = Engine(source_path = source_path, testcase_path = testcase_path, output_path = output_path)
			try:
				id = testcase.id
				engine.process()
			except Engine.CompileError:
				 response[id] = 'error'
			except Engine.TimeOut:
				response[id] = 'TLE'
			else:
				if engine.check_output(output_path):
					response[id] = 'AC'
				else:
					response[id] = 'WA'

		return JsonResponse(response)
		# print ( testcase_path )
		# submission.save()
		# microservice and celery
		return HttpResponse('passed')
	else:
		return HttpResponse('failed')