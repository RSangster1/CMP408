import psutil
import sys
import boto3
import json
import subprocess
import platform
from datetime import datetime


#Get data about the pi
def getData():

    current_datetime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    cpu_percent =  psutil.cpu_percent()
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    disk_total = psutil.disk_usage('/').total
    temperature = psutil.sensors_temperatures().get('cpu_thermal', [])[0].current
    memory_total = psutil.virtual_memory().total

    # in JSON format
    pi_data = {
       'date/time': current_datetime,
       'cpu_percent': cpu_percent,
       'cpu_count': cpu_count,
       'cpu_freq': cpu_freq,
       'disk_total': disk_total,
       'temperature': temperature,
       'memory_total': memory_total
    }

    with open('pi_data.json', 'w')as file:
         json.dump(pi_data, file)

    return json.dumps(pi_data)

#upload the json file to amazon ec2 instance
def upload_to_aws():


   username = "ec2-user"
   data_file = "/home/pi/pi_data.json"
   ip_address = "44.207.97.0"
   path = "/home/ec2-user"


   #rsync command
   rsync = [
       "rsync",
       "-av",
       "-e", "ssh -i /home/pi/CMP408.pem",
       data_file,
       "{}@{}:{}".format(username, ip_address, path)
   ]



   try:
       subprocess.check_output(rsync)
       print("Upload Successful")
       response = "OK"
       return response
   except subprocess.CalledProcessError as e:
       print("{e}")

response = upload_to_aws()

print("getting data")
pi_data = getData()
print("uploading to AWS")
upload_to_aws()
if response != "OK":
   subprocess.check_call(['sudo', 'insmod', 'led.ko'])
   subprocess.check_call(['sudo', 'rmmod', 'led.ko'])
else:
   subprocess.check_call(['sudo', 'insmod', 'lednot.ko'])
   subprocess.check_call(['sudo', 'rmmod', 'lednot.ko'])

