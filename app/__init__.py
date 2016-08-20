import re

from flask import (
    jsonify,
    Flask,
)

import exceptions as exc


def re_sub(s, find, replace):
    return re.sub(find, replace, s)


def create_app():
    app = Flask(__name__)
    app.debug = True

    from app.views import frontend
    from app.views import api

    app.register_blueprint(frontend)
    app.register_blueprint(api, url_prefix='/api')

    app.jinja_env.filters['re_sub'] = re_sub

    init_error_handlers(app)

    return app


def init_error_handlers(app):

    @app.errorhandler(exc.WebServiceError)
    def base_error_handler(err):
        return jsonify(reason=err.reason, code=err.code), err.code

    @app.errorhandler(404)
    def not_found_handler(err):
        return base_error_handler(exc.NotFound())

    @app.errorhandler(500)
    def exception_handler(err):
        return base_error_handler(exc.ServerError())
