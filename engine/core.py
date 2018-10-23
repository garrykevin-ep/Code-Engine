from pathlib import Path
import subprocess


class Engine():

	def __init__(self, source_path, testcase_path, output_path, timeout=1):
		self.source_path = source_path
		self.testcase_path = testcase_path
		self.output_path = output_path
		self.timeout = timeout

	def process(self):
		with open(self.output_path,'w') as output_file, open(self.testcase_path,'r') as testcase_file:
			try:
				completed_process = subprocess.run(["python3", self.source_path ], timeout = self.timeout,\
					stdout = output_file,stdin = testcase_file,stderr=output_file)
				if completed_process.returncode != 0:
					raise self.CompileError
			except subprocess.TimeoutExpired:
				raise self.TimeOut

	class TimeOut(Exception):
		pass

	class CompileError(Exception):
		pass




def main():
	base_dir = Path(__file__).resolve().parent
	source_path = base_dir / 'source' / 'a.py'
	testcase_path = base_dir / 'testcase' / 'a.input'
	output_path = base_dir / 'output' / '1_1'
	engine = Engine(source_path = source_path, testcase_path = testcase_path, output_path = output_path)
	try:
		engine.process()
	except Engine.CompileError:
		# return error
		print ("error..")
	except Engine.TimeOut:
		print ("time out")
		# return "time out"
	# f = open(source_code)
	# print (f.readlines())


main()
