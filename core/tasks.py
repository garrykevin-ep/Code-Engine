from celery import shared_task,current_task
from pathlib import Path
from engine.core import Engine
from django.conf import  settings
from .models import TestCase
@shared_task
def execute_testcases(submission_file, submission_id,problem):
	base_dir = Path(settings.MEDIA_ROOT).resolve()
	source_path = base_dir / submission_file
	testcases = TestCase.objects.filter(problem=problem)
	response = {}
	for testcase in testcases:
			testcase_path = base_dir / testcase.testcase.name
			output_path = base_dir / 'user_output' /( str(submission_id) + str(testcase.id))
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
			current_task.update_state(state="PROGRESS",
				meta =  response )
	return response

@shared_task
def add(n):
	result = 0
	for adder in range(1,n):
		result += adder
		status = 'added till {} the is result {}'.format(adder,result)
		current_task.update_state(state="PROGRESS",meta={'status' : status})
	return result

