from flask import Flask
from .database import db
from flask_login import LoginManager, current_user

login_manager = LoginManager()
def create_app():
    app = Flask(__name__)

    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    import app.mainmodule.controllers as mainmodule

    app.register_blueprint(mainmodule.module)

    login_manager.init_app(app)

    @app.context_processor
    def utility_processor():
        def get_current_user():
            return current_user

        return dict(get_current_user=get_current_user)

    return app
