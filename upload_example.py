# upload_example.py
# Author: Daniel Schulz
# Project: Capstone TA-IP 2018 (Watermelon Capstone)
# Description: Example of how to upload images & data.

import requests
import datetime
import os
import uuid
import json

# URL of Flask server (assuming localhost)
url = "http://127.0.0.1:5000/upload"
#url = "http://watermelon-flask.hp7jzffnep.ap-southeast-2.elasticbeanstalk.com/upload"
# File array for request
filename = 'test.jpg'
files = {'files': open(filename, 'rb')}
ripe = 'T'
datetime_result = datetime.datetime.now()
unique_id = str(uuid.uuid4()) + os.path.splitext(filename)[-1]
# Sample Spectrometer reading
spect = [
    121, 121, 951, 978, 977, 965, 969, 963, 956, 966, 979, 954, 965, 964, 970, 970, 975, 972, 964, 958, 958, 959,
    960, 973, 964, 971, 956, 942, 967, 984, 974, 951, 979, 958, 964, 978, 972, 973, 984, 997, 988, 1000, 998, 1007,
    1010, 1003, 1009, 1004, 1009, 1003, 1010, 1006, 1005, 1008, 1001, 1007, 1010, 1005, 1001, 1004, 1010, 1010, 1012,
    1001, 1008, 1005, 1010, 1004, 1002, 998, 1007, 1004, 1001, 997, 1001, 1005, 1003, 1003, 1000, 1005, 1005, 994,
    1000, 1007, 1004, 1001, 998, 995, 1001, 988, 997, 1001, 997, 1001, 998, 998, 1003, 999, 999, 994, 996, 1001, 999,
    1004, 1006, 1001, 1001, 996, 993, 1006, 1006, 1003, 1003, 1005, 1001, 1006, 1003, 1002, 997, 1000, 1001, 1002,
    1004, 996, 994, 1001, 1003, 1001, 1006, 1002, 1000, 1000, 1003, 1004, 1007, 1006, 1002, 1003, 1002, 1005, 1007,
    1003, 1006, 1004, 1001, 1008, 1004, 1011, 1007, 1002, 1006, 1009, 1003, 997, 1007, 1004, 1002, 1009, 1005, 996,
    1002, 1001, 997, 1004, 999, 999, 1002, 1006, 1007, 1000, 1006, 1003, 1007, 1000, 1012, 1003, 1008, 1006, 1014,
    1000, 1002, 1002, 1000, 1003, 998, 1004, 1003, 1005, 1002, 1005, 1008, 1008, 995, 1000, 1003, 1007, 1006, 1003,
    1009, 1007, 1013, 1003, 1010, 1001, 1004, 1002, 1009, 1005, 1015, 1011, 1002, 996, 989, 987, 985, 979, 972, 950,
    953, 943, 927, 909, 901, 890, 880, 897, 906, 885, 872, 882, 889, 881, 855, 867, 863, 858, 869, 888, 884, 870,
    893, 896, 921, 893, 884, 872, 863, 863, 870, 880, 899, 880, 822, 830, 877, 815, 799, 779, 808, 787, 765, 770,
    789, 768, 790, 805, 754, 746, 775, 796, 745, 758, 769, 740, 744, 786, 791, 761, 752, 752, 768, 757, 794, 744,
    744, 772, 778, 731
]
# Laser was OFF, LED was ON
la = 'F'
le = 'T'

data = {'r': ripe, 'd': datetime_result, 'k': unique_id, 'spe': json.dumps(spect), 'le': le, 'la': 'la'}
# Add both the file image to upload, and accompanying data and POST
r = requests.post(url, files=files, data=data)
print(str(r.content))
