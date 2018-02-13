import os
import sys
import time
import getpass
import requests
import argparse
import csv
from bs4 import BeautifulSoup
from shutil import copyfile

#create dictionaries for variable conversion
pipeline_to_int = {"volBrain":1, "CERES":3}
get_genre = {"":"--", "F": "Female" , "M":"Male"}

#argument declarations
parser = argparse.ArgumentParser(description="automatic bot to upload files to volbrain")
parser.add_argument('-s','--batch_size', action="store", default=10, type=int,
                    help='number of images to upload simultaneously (default: %(default)s)')
parser.add_argument('-w','--wait', action="store", default=300, type=int,
                    help='Number of seconds to wait between the batches of images(default: %(default)s)')
parser.add_argument('-p','--pipeline',
                    default="volBrain",
                    const="volBrain",
                    nargs='?',
                    choices=["volBrain", "CERES"],
                    help='pipeline (volBrain, CERES) (default: %(default)s)')
parser.add_argument('files', type=argparse.FileType('r'),
                    help='tsv file with all path images, age (integer number) and gender of pacient')

args = parser.parse_args()

#open the file containing the images list
files = csv.reader(args.files, delimiter='\t')
batch_size = args.batch_size
wait = args.wait
pipeline_in_text= args.pipeline

#load initial url
base_url ="http://volbrain.upv.es/"
page = "login.php"
#build the dictionary for sending the login data
payload = {'email':'xxxxx@upv.es', 'password':'xxxxxxx'}

stop = False
actual_file = 0

#create a session so we maintain the user logged
s = requests.Session()
#send the login info
r = s.post(base_url+page, payload)

#get the response page after loggin in
c = r.content
soup = BeautifulSoup(c,"lxml")

#select the upload form
form = soup.find(id="upload_form")

#check if the form exist, if not, it means something went wrong. Probably, the data is incorrect
if form is None:
    print("wrong user information")
    sys.exit(0)
next_page = form["action"]

file_in_batch = 0

# iterate over all lines from the file to upload all th files.
for line in files:

	# if the number of files we uploaded are bigger than a certain ammount, wait some time before uploading again
	if file_in_batch>= batch_size:
		print("Batch completed")
		print("Waiting "+ str(wait) +" seconds")
		s.close()
		time.sleep(wait)
		s = requests.Session()
		r = s.post(base_url+page, payload)

		c = r.content
		soup = BeautifulSoup(c,"lxml")

		form = soup.find(id="upload_form")
		next_page = form["action"]
		file_in_batch = 0

	print("Image " + str(file_in_batch) + "("+str(actual_file)+")" + " of " + str(batch_size))
	# build the upload information
	image_form = {"pipeline":str(pipeline_to_int[pipeline_in_text]),
		 "patientssex":get_genre[line[2]], "patientsage":str(line[1])}

	# to keep track of the pipeline in the name, we need to rename the file
	#file_path_splitted = line[0].split('/')
	#new_file = "/".join(file_path_splitted[:-1]) + '/' + pipeline_in_text + "_" + file_path_splitted[-1]
	new_file=line[0]
	#copyfile(line[0], new_file)
	with open(new_file,'rb') as file_to_upload:
		# as we need to provide the info about the files upload apart, we build now the regarding dictionary
		upload_files = {"uploaded_file":file_to_upload}

		# send the petition to upload the fhe file
		r = s.post(base_url+next_page,files=upload_files, data=image_form)

		#here, we should do some checkings

	# remove the file we created
	# os.remove(new_file)

	file_in_batch+=1
	actual_file+=1
	time.sleep(10)

# when we are done, check if we didn't complete a batch and close the session in that case
if file_in_batch < batch_size:
    s.close()
