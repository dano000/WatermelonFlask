# manage.py
# Author: Daniel Schulz
# Project: Capstone TA-IP 2018 (Watermelon Capstone)
# Description: For managing migrations for Flask app.

from flask_migrate import Manager, Migrate, MigrateCommand

from application import application, Config
from models import db

app.config.from_object(Config)

migrate = Migrate(application, db)
manager = Manager(application)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()