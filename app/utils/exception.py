from flask import current_app


def handle_exception(e: Exception):
    current_app.logger.exception('Uncaught exception')
    return 'Internal Server Error', 500
