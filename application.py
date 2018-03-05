# app.py
# Author: Daniel Schulz
# Project: Capstone TA-IP 2018 (Watermelon Capstone)
# Description: Flask Server for handling image/data uploads to AWS.

from flask import Flask, request
import boto3
import os
from models import db, Result

# Initialise flask factory and database
application = Flask(__name__)
db.init_app(application)


# Basic configuration for the application.
class Config(object):
    S3_BUCKET = 'watermelons-training'
    S3_KEY = os.environ['S3_KEY']
    S3_SECRET = os.environ['S3_SECRET']
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    SECRET_KEY = os.urandom(32)
    DEBUG = True
    PORT = 5000

    POSTGRES = {
        'user': os.environ['RDS_USERNAME'], # 'postgres',
        'pw': os.environ['RDS_PASSWORD'], # 'postgres',
        'db': os.environ['RDS_DB_NAME'],  # 'watermelon_dev',
        'host': os.environ['RDS_HOSTNAME'],  # 'localhost',
        'port': os.environ['RDS_PORT'] # '5432',
    }

    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

# Setup config
application.config.from_object(Config)

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Make a connection to AWS S3 storage bucket to be for images.
s3 = boto3.resource(
   "s3",
   aws_access_key_id=Config.S3_KEY,
   aws_secret_access_key=Config.S3_SECRET
)


# Define the route that will accept uploads (images and measurement data).
@application.route('/upload', methods= ['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['files']
        r = True if request.form['r'] == 'T' else False
        d = request.form['d']
        k = request.form['k']
        print("{} {}: Ripe = {}".format(d, k, r))
        s3_return = s3.Bucket(Config.S3_BUCKET).put_object(Key=k, Body=f.read())
        result = Result(s3_key=k, etag=s3_return.e_tag, ripe=r, timestamp=d)
        db.session.add(result)
        db.session.commit()
        return str(result)
    else:
        return("GET status 200")



# Run the application
if __name__ == '__main__':
    application.debug = True
    application.run()
