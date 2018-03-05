# WatermelonFlask

## Instructions

##### Note: This assumes you have a Postgresql installation already and that all environment variables (eg. S3_KEY / S3_SECRET) are set!
##### Assumes you are working with python 3 (otherwise replace all instances of `python` with `python3` below).

* Install a python 3.6 virtualenv: `python -m venv flask_venv`
* Activate venv: `flask_venv\Scripts\activate`
* Install dependencies: `python -m pip install -r requirements.txt`
* Create database with postgres: `createdb watermelon_dev`
* Update the database with the migrations: `python manage.py upgrade`
* Launch the app: `python app.py`
* Start uploading using: `python upload_example.py` in a separate console.

## Migrations
##### It's important that migrations are kept consistent, so that there is a consistent database. When you are updating things in `models.py` ensure that:
* A migration file is generated: `python manage.py migrate`
* The migration is applied: `python manage.py upgrade`
* A git commit and upload is performed *BEFORE* going on with more work: eg. `git commit -m "Added spectrometer reading column to results table.`
