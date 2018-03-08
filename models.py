# models.py
# Author: Daniel Schulz
# Project: Capstone TA-IP 2018 (Watermelon Capstone)
# Description: For managing model definitions for Flask app.

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
db = SQLAlchemy()


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    s3_key = db.Column(db.String())
    etag = db.Column(db.String())
    ripe = db.Column(db.Boolean())
    timestamp = db.Column(db.DateTime())
    readings = db.relationship('Reading', backref='result', lazy='dynamic')

    # Initializer, when result is inserted.
    def __init__(self, s3_key, etag, ripe, timestamp):
        self.s3_key = s3_key
        self.etag = etag
        self.ripe = ripe
        self.timestamp = timestamp

    # Returned value when inserted - this will be the printed result.
    def __repr__(self):
        return '<id {}, timestamp {}, s3_key {}, ripe {}, etag {}>'.format(self.id, self.timestamp, self.s3_key, self.ripe, self.etag)


class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime())
    reading = db.Column(ARRAY(db.Integer))
    laser = db.Column(db.Boolean())
    led = db.Column(db.Boolean())
    result_id = db.Column(db.Integer, db.ForeignKey('result.id'))

