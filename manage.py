# manage.py
# Author: Daniel Schulz
# Project: Capstone TA-IP 2018 (Watermelon Capstone)
# Description: For managing migrations for Flask app.

# Original Source: https://blog.miguelgrinberg.com/post/flask-migrate-alembic-database-migration-wrapper-for-flask

# Usage:    python manage.py db migrate # To generate the database migrations (of what you want the changes to be).
#           python manage.py db upgrade # Perform an upgrade to a newer migration (execute a new migration on db).

from flask_migrate import Manager, Migrate, MigrateCommand

from application import application, Config
from models import db

application.config.from_object(Config)

migrate = Migrate(application, db)
manager = Manager(application)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()