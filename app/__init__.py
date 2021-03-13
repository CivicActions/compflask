__version__ = "0.1.0"

from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    csrf.init_app(app)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    from app.auth.controllers import auth as auth_module
    from app.pages.controllers import page

    app.register_blueprint(auth_module)
    app.register_blueprint(page)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from app.auth.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/")
    def index():
        return render_template("page/index.html")

    return app
