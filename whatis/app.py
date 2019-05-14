from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from whatis import config

def create_app():
    app = Flask(__name__)
    # whatis.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config.from_object(config)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    from whatis.routes.slack.slack_route import slack_blueprint
    app.register_blueprint(slack_blueprint, url_prefix='/slack')

    from whatis.routes.web.web_route import web_blueprint
    app.register_blueprint(web_blueprint, url_prefix='/whatis')

    return app
