from .api import api_bp


def register_blueprint(app):
    app.register_blueprint(api_bp, url_prefix='/api/v1')
