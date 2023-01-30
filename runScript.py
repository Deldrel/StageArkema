import subprocess
import time


def run_script():
	result = subprocess.run(["python", "sendMQTT.py"])
	return result_is_file
	

for i in range (300):
	try:
		result = run_script()
		if result.returncode == 0:
			break
	except:
		continue
		
	time.sleep(2)
