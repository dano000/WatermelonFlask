# models.py
# Author: Daniel Schulz
# Project: Capstone TA-IP 2018 (Watermelon Capstone)
# Description: For managing model definitions for Flask app.

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
db = SQLAlchemy()


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pi_id = db.Column(db.Integer)
    pi_serial = db.Column(db.String())
    s3_key = db.Column(db.String())
    etag = db.Column(db.String())
    ripe = db.Column(db.Boolean())
    timestamp = db.Column(db.DateTime())
    readings = db.relationship('Reading', backref='result', lazy='dynamic')
    weather = db.Column(db.String())
    s3_audio_key = db.Column(db.String())
    etag_audio = db.Column(db.String())
    slap_type = db.Column(db.String())

    # Initializer, when result is inserted.
    def __init__(self,pi_id,pi_serial, s3_key, etag, ripe, timestamp, weather, s3_audio_key,etag_audio, slap_type):
        self.pi_id = pi_id,
        self.pi_serial = pi_serial,
        self.s3_key = s3_key
        self.etag = etag
        self.ripe = ripe
        self.timestamp = timestamp
        self.weather = weather
        self.s3_audio_key = s3_audio_key
        self.etag_audio = etag_audio
        self.slap_type = slap_type

    def to_json(self):
        return dict(
            id=self.id,
            pi_id = self.pi_id,
            pi_serial = self.pi_serial,
            s3_key = self.s3_key,
            etag = self.etag,
            ripe = self.ripe,
            timestamp = self.timestamp,
            readings = [i.to_json() for i in self.readings],
            weather = self.weather,
            s3_audio_key = self.s3_audio_key,
            etag_audio = self.etag_audio,
            slap_type = self.slap_type
        )

    # Returned value when inserted - this will be the printed result.
    def __repr__(self):
        return '<id {}, pi_id {}, timestamp {}, s3_key {}, ripe {}, etag {}>'.format(self.id,self.pi_id, self.timestamp, self.s3_key, self.ripe, self.etag)


class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pi_id = db.Column(db.Integer)
    pi_serial = db.Column(db.String())
    timestamp = db.Column(db.DateTime())
    reading = db.Column(ARRAY(db.Integer))
    laser = db.Column(db.Boolean())
    led = db.Column(db.Boolean())
    uv = db.Column(db.Boolean())
    result_id = db.Column(db.Integer, db.ForeignKey('result.id'))

    def to_json(self):
        return dict(
            id=self.id,
            pi_id = self.pi_id,
            pi_serial = self.pi_serial,
            timestamp = self.timestamp,
            reading = self.reading,
            laser = self.laser,
            led = self.led,
            uv = self.uv,
            result_id = self.result_id
        )