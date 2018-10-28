from pathlib import Path
import subprocess
# from itertools  import izip

class Engine():

	def __init__(self, source_path, testcase_path, output_path, timeout=6):
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
					self.result = "ERROR"
					raise self.CompileError
			except subprocess.TimeoutExpired:
				self.result = 'TLE'
				raise self.TimeOut

	def check_output(self,expected_output_path):
		
		with open(expected_output_path,'r') as expected_output , open(self.output_path,'r') as user_output :
			if user_output.readlines() == expected_output.readlines():
				self.result = 'AC'
				return True
			else:
				self.result = 'WA'
				return False
		# 	user = user_output.readlines()
		# 	exp = expected_output.readlines()
		# 	if len(user) == 0 and len(exp) != 0:
		# 		return False
		# 	for linef1, linef2 in zip(user,exp):
		# 		linef1 = linef1.rstrip('\r\n')
		# 		linef2 = linef2.rstrip('\r\n')
		# 		if linef1 != linef2:
		# 			return False
		# 	return True
			
			

	class TimeOut(Exception):
		pass

	class CompileError(Exception):
		pass




def main():
	base_dir = Path(__file__).resolve().parent
	source_path = base_dir / 'source' / 'a.py'
	testcase_path = base_dir / 'testcase' / 'a.input'
	output_path = base_dir / 'output' / '1_1'
	expected_output = base_dir / 'expet'
	engine = Engine(source_path = source_path, testcase_path = testcase_path, output_path = output_path)
	try:
		engine.process()
	except Engine.CompileError:
		# return error
		print ("error..")
	except Engine.TimeOut:
		print ("time out")
	print (engine.check_output(expected_output))
	


main()
