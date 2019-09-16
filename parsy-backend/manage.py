from application import application
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flaskApp import db


migrate = Migrate(application, db)
manager = Manager(application)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

###NOTE: Run manage.py db migrate, then DO NOT RUN UPGRADE BEFORE COMMENTING OUT IN THE FOLDER
###THE PART ABOUT DROPPING THE EXISTING TABLES. OTHERWISE, THIS WILL DESTROY YOUR
### HARD EARNED DATA. AFTER COMMENTING out you can run manage.py db upgrade
