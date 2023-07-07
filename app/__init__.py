from flask import Flask
from .database import db

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    import app.mainmodule.controllers as mainmodule

    app.register_blueprint(mainmodule.module)

    return app
