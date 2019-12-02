from werkzeug.exceptions import NotFound, MethodNotAllowed

from ..utils.http import result_formatter
from flask import jsonify, current_app


class BusinessLogicException(Exception):

    def __init__(self, message: str, status: int, data: dict = None):

        self.status = status
        self.message = message
        self.data = data

    def to_result_bean(self) -> dict:

        if self.data is None:
            return result_formatter(self.message, self.status)
        else:
            return result_formatter(self.data, self.status, self.message)


def handle_api_error(e: Exception):
    if isinstance(e, BusinessLogicException):
        return jsonify(e.to_result_bean()), 200
    if isinstance(e, NotFound):
        return jsonify(result_formatter('URL Not Found', 404))
    if isinstance(e, MethodNotAllowed):
        return jsonify(result_formatter('Method Not Allowed', 404))
    current_app.logger.exception('Uncaught Exception')
    return jsonify(result_formatter('Internal Server Error', 500))
