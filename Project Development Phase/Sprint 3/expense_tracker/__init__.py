import os

from flask import Flask, g, redirect, render_template, url_for
from expense_tracker.auth import login_required
from expense_tracker.db import get_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    UPLOAD_FOLDER = 'receipts'
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5mb

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        os.makedirs(UPLOAD_FOLDER)
    except OSError:
        pass

    from . import db
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.bp)
    from . import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')
    from . import transaction
    app.register_blueprint(transaction.bp)

    # Index page
    @app.route('/')
    def index():
        if g.user:
            return redirect(url_for('dashboard.index'))
        return render_template('index.html')
    return app
