# app.py
# Author: Daniel Schulz
# Project: Capstone TA-IP 2018 (Watermelon Capstone)
# Description: Flask Server for handling image/data uploads to AWS.

from flask import Flask, request, render_template, jsonify, url_for
import boto3
import os
from models import db, Result, Reading
from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import ARRAY, array
import json
from flask_bootstrap import Bootstrap
from flask_basicauth import BasicAuth
import tensorflow as tf
import numpy as np
import model
import cv2
import datetime

from spectrogram import generate_html_spectrogram, get_average_spectrogram

# Initialise flask factory and database
application = Flask(__name__)
application.config['BASIC_AUTH_USERNAME'] = 'watermelons'
application.config['BASIC_AUTH_PASSWORD'] = 'watermelons'

basic_auth = BasicAuth(application)
Bootstrap(application)
db.init_app(application)

if(os.environ['RDS_HOSTNAME'] == 'localhost'):
    application.config['BOOTSTRAP_SERVE_LOCAL'] = True


# Basic configuration for the application.
class Config(object):
    S3_BUCKET = 'watermelons-training'
    S3_KEY = os.environ['S3_KEY']
    S3_SECRET = os.environ['S3_SECRET']
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
    S3_ENDPOINT = "https://s3-ap-southeast-2.amazonaws.com/{}/".format(S3_BUCKET)
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


class tfPredictor():
    def __init__(self):
        self.predictor = tf.estimator.Estimator(
            model_fn=model.model, model_dir="./Model/")

    def image_process(self, imagefile):
        np_array = np.fromstring(imagefile, np.uint8)
        np_image = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)
        return cv2.resize(np_image, (28, 28))

    def eval_result(self, image):
        eval_data = np.reshape(self.image_process(image),[1,28,28,1]).astype(np.float32)
        predict_input_fn = tf.estimator.inputs.numpy_input_fn(
             x={"x": eval_data},
             num_epochs=1,
             shuffle=False)
        eval_results = list(self.predictor.predict(input_fn=predict_input_fn))
        return eval_results


# Initialise predictor
predictor = tfPredictor()


def string_t(string):
    return True if string == 'T' else False

# Define the route that will accept uploads (images and measurement data).
@application.route('/upload', methods= ['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f_image = request.files.getlist('image')[0]
        f_audio = request.files.getlist('audio')[0]
        pi_id = request.form['pi_i']
        r_ids = json.loads(request.form['r_ids'])
        pi_serial = request.form['pi_s']
        r = True if request.form['r'] == 'T' else False
        d = request.form['d']
        k = request.form['k']
        i = request.form['i']
        w = request.form['w']
        s = request.form['s']
        spect = list(map(lambda x: array(x), json.loads(request.form['spe'])))
        laser = list(map(lambda x: string_t(x), json.loads(request.form['la'])))
        led = list(map(lambda x: string_t(x), json.loads(request.form['le'])))
        uv = list(map(lambda x: string_t(x), json.loads(request.form['uv'])))
        read_image = f_image.read()
        read_audio = f_audio.read()
        s3_image_return = s3.Bucket(Config.S3_BUCKET).put_object(Key=k, Body=read_image)
        s3_audio_return = s3.Bucket(Config.S3_BUCKET).put_object(Key=i, Body=read_audio)
        if(len(spect[0]) and len(spect)):
            result = Result(pi_id=pi_id, pi_serial=pi_serial, s3_key=k, etag=s3_image_return.e_tag, ripe=r, timestamp=d, weather=w, slap_type=s,s3_audio_key=i, etag_audio=s3_audio_return.e_tag)
            db.session.add(result)
            for i,s in enumerate(spect):
                reading = Reading(id=r_ids[i],timestamp=d,pi_id=pi_id,pi_serial=pi_serial,reading=db.cast(s, ARRAY(db.Integer)), laser=laser[i], led=led[i], uv=uv[i])
                result.readings.append(reading)
                db.session.add(reading)
        else:
            result = Result(pi_id=pi_id, pi_serial=pi_serial, s3_key=k, etag=s3_image_return.e_tag, ripe=r, timestamp=d, weather=w, slap_type=s,s3_audio_key=i, etag_audio=s3_audio_return.e_tag)
            db.session.add(result)

        db.session.commit()
        #eval_result = predictor.eval_result(read_file)

        #print("result:",str(result))
        #print("eval:",str(eval_result))
        return (str(result))
    else:
        return("POST API Endpoint only")


@application.route('/reading/avg/normal/<reading_start_id>')
@basic_auth.required
def reading_avg_normal(reading_start_id):
    if request.method == 'GET':

        normal_spects = db.session.query(Result).join('readings').filter(Reading.uv == False, Reading.led == False, Reading.laser == False, Reading.id >= reading_start_id).all()

        normal_avg_spects = [get_average_spectrogram(list(map(lambda x: x.reading, r.readings))).tolist() for r in normal_spects]
        normal_avg_spects_ripe = [(1 if r.ripe else 0) for r in normal_spects]

        return (json.dumps(
            {'spects': normal_avg_spects,
                'features': normal_avg_spects_ripe
             }
        ))

@application.route('/reading/avg/uv/<reading_start_id>')
@basic_auth.required
def reading_avg_uv(reading_start_id):
    if request.method == 'GET':

        uv_spects = db.session.query(Result).join('readings').filter(Reading.uv == True, Reading.led == False, Reading.laser == False, Reading.id >= reading_start_id).all()

        uv_avg_spects = [get_average_spectrogram(list(map(lambda x: x.reading, r.readings))).tolist() for r in uv_spects]
        uv_avg_spects_ripe = [(1 if r.ripe else 0) for r in uv_spects]

        return(json.dumps(
            {'spects': uv_avg_spects,
                'features': uv_avg_spects_ripe
             }
        ))

@application.route('/result/id/<id>')
@basic_auth.required
def view_result(id):
    if request.method == 'GET':
        result = Result.query.filter_by(id=id).first_or_404()
        if(result):
            average_spect = get_average_spectrogram(list(map(lambda x: x.reading, result.readings)))
        else:
            average_spect = ''

        is_picture = True if (result.s3_key[-4:] == '.jpg') else False
        is_video = True if (result.s3_key[-4:] == '.mp4' or result.s3_key[-5:] == '.mpeg' or result.s3_key[-5:] == '.h264') else False

        try:
            s3_audio_url = Config.S3_ENDPOINT + result.s3_audio_key
        except:
            s3_audio_url = Config.S3_ENDPOINT + ''

        return render_template("show_result.html",result=result,html_spect=generate_html_spectrogram(average_spect), s3_image_url=Config.S3_ENDPOINT + result.s3_key, s3_audio_url=s3_audio_url, is_picture=is_picture, is_video=is_video)


@application.route('/result/summary')
@basic_auth.required
def summary():
    page = request.args.get('page', 1, type=int)
    all_results = db.session.query(Result).order_by(desc(Result.timestamp)).paginate(
        page, 10, False)

    last_result = Result.query.all()[-1]

    if (last_result):
        average_spect = get_average_spectrogram(list(map(lambda x: x.reading, last_result.readings)))
    else:
        average_spect = ''

    try:
        s3_audio_url = Config.S3_ENDPOINT + last_result.s3_audio_key
    except:
        s3_audio_url = Config.S3_ENDPOINT + ''

    is_picture = True if (last_result.s3_key[-4:] == '.jpg') else False
    is_video = True if (last_result.s3_key[-4:] == '.mp4') else False

    t_delta = (datetime.datetime.now() - last_result.timestamp)

    hours = t_delta.total_seconds() // 3600
    minutes = (t_delta.total_seconds() % 3600) // 60
    seconds = t_delta.total_seconds() % 60

    time_since_last_update = "{hours:.0f} Hours, {minutes:.0f} minutes and {seconds:.0f} seconds".format(hours=hours,minutes=minutes, seconds=seconds)

    next_url = url_for('summary', page=all_results.next_num) if all_results.has_next else None
    prev_url = url_for('summary', page=all_results.prev_num) if all_results.has_prev else None

    return render_template("show_result_summary.html", time_since_last_update=time_since_last_update, all_results=all_results,last_result=last_result, html_spect=generate_html_spectrogram(average_spect), s3_image_url=Config.S3_ENDPOINT + last_result.s3_key, s3_audio_url=s3_audio_url, is_picture=is_picture, is_video=is_video,  next_url=next_url, prev_url=prev_url)


@application.route('/result/pi_id/<pi_id>')
@basic_auth.required
def view_result_pi_id(pi_id):
    if request.method == 'GET':
        result = Result.query.filter_by(pi_id=pi_id).first_or_404()
        if (result):
            average_spect = get_average_spectrogram(list(map(lambda x: x.reading, result.readings)))
        else:
            average_spect = ''

        is_picture = True if (result.s3_key[-4:] == '.jpg') else False
        is_video = True if (result.s3_key[-4:] == '.mp4') else False

        try:
            s3_audio_url = Config.S3_ENDPOINT + result.s3_audio_key
        except:
            s3_audio_url = Config.S3_ENDPOINT + ''

        return render_template("show_result.html",result=result, html_spect=generate_html_spectrogram(average_spect), s3_image_url=Config.S3_ENDPOINT + result.s3_key, s3_audio_url=s3_audio_url, is_picture=is_picture, is_video=is_video)


@application.route('/reading/id/<id>')
@basic_auth.required
def view_reading(id):
    if request.method == 'GET':
        reading = Reading.query.filter_by(id=id).first_or_404()
        return render_template("show_reading.html",reading=reading, html_spect=generate_html_spectrogram(reading.reading))


@application.route('/result/json/pi/<pi_id>')
@basic_auth.required
def json_result_pi_id(pi_id):
    if request.method == 'GET':
        result = Result.query.filter_by(pi_id=pi_id).first_or_404()
        return jsonify(result.to_json())


@application.route('/result/json/id/<id>')
@basic_auth.required
def json_result(id):
    if request.method == 'GET':
        result = Result.query.filter_by(id=id).first_or_404()
        return jsonify(result.to_json())


@application.route('/reading/json/<id>')
@basic_auth.required
def json_reading(id):
    if request.method == 'GET':
        reading = Reading.query.filter_by(id=id).first_or_404()
        return jsonify(reading.to_json())


@application.route('/result/all')
@basic_auth.required
def get_all_results():
    all_json = [i.to_json() for i in Result.query.all()]
    return jsonify(json_list=all_json)


@application.route('/reading/all')
@basic_auth.required
def get_all_readings():
    all_json = [i.to_json() for i in Reading.query.all()]
    return jsonify(json_list=all_json)


# Run the application
if __name__ == '__main__':
    application.debug = True
    application.run()
