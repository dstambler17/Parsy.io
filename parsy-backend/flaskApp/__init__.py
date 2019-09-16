from flask import Flask
#from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flaskApp.conf import OfflineConfiguration, OnlineConfiguration
from flask_cors import CORS, cross_origin

#db = MySQL()
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(offline=False):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    if offline:
        app.config.from_object(OfflineConfiguration)
    else:
        app.config.from_object(OnlineConfiguration)

    db.init_app(app)
    bcrypt.init_app(app)

    from flaskApp.course.views import course
    from flaskApp.user.views import user
    from flaskApp.exam.views import exam
    from flaskApp.helpSession.views import helpSession
    from flaskApp.searchOption.views import searchOption
    from flaskApp.classMeeting.views import classMeeting
    from flaskApp.assignment.views import assignment
    app.register_blueprint(course, url_prefix='/course')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(exam, url_prefix='/exam')
    app.register_blueprint(searchOption, url_prefix='/searchOption')
    app.register_blueprint(classMeeting, url_prefix='/classMeeting')
    app.register_blueprint(helpSession, url_prefix='/helpSession')
    app.register_blueprint(assignment, url_prefix='/assignment')

    return app
