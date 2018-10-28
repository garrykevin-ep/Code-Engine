from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from engine.core import Engine
from pathlib import Path
import uuid
import os

def save_file(in_memeroy_file,suffix=''):
	path = default_storage.save('tmp/' + str(uuid.uuid1()) + suffix , ContentFile(in_memeroy_file.read()))
	file = os.path.join(settings.MEDIA_ROOT, path)
	return file

def remove(path):
	os.unlink(path)

def run(request):
	if request.method == 'GET':
		return render(request,'service/run.html')
	else:
		source_code = request.FILES['source_code']
		test_case = request.FILES['test_case']
		expected_out = request.FILES['expected_out']
		
		source_code = save_file(source_code,'.py')
		test_case = save_file(test_case)
		expected_out = save_file(expected_out)

		output_path = Path(settings.MEDIA_ROOT) / 'tmp/' / str(uuid.uuid1())
		
		engine = Engine(source_path = source_code, testcase_path = test_case, output_path = output_path)
		
		try:
			engine.process()
		except :
			pass
		else:
			engine.check_output(expected_out)

		# remove(source_code)
		# remove(test_case)
		# remove(expected_out)
		# remove(output_path)

		return HttpResponse(engine.result)
