# upload_example.py
# Author: Daniel Schulz
# Project: Capstone TA-IP 2018 (Watermelon Capstone)
# Description: Example of how to upload images & data.

import requests
import datetime
import os
import uuid

# URL of Flask server (assuming localhost)
#url = "http://127.0.0.1:5000/upload"
url = "http://watermelon-flask.hp7jzffnep.ap-southeast-2.elasticbeanstalk.com/upload"
# File array for request
filename = 'test.jpg'
files = {'files': open(filename, 'rb')}
ripe = 'T'
datetime_result = datetime.datetime.now()
unique_id = str(uuid.uuid4()) + os.path.splitext(filename)[-1]

data = {'r': ripe, 'd': datetime_result, 'k': unique_id}
# Add both the file image to upload, and accompanying data and POST
r = requests.post(url, files=files, data=data)
print(str(r.content))
