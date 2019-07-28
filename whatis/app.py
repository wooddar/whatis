from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.db = db
    migrate = Migrate(app, db)
    from routes.slack.slack_route import slack_blueprint

    app.register_blueprint(slack_blueprint, url_prefix="/slack")

    from routes.web.web_route import web_blueprint

    app.register_blueprint(web_blueprint, url_prefix="/whatis")

    @app.route("/ping")
    def healthcheck():
        return "pong"

    return app
