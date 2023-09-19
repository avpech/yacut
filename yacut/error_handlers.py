from http import HTTPStatus
from typing import Tuple

from flask import Response, jsonify, render_template

from yacut import app, db
from yacut.exceptions import InvalidAPIUsage


@app.errorhandler(HTTPStatus.NOT_FOUND.value)
def page_not_found(error: Exception) -> Tuple[str, HTTPStatus]:
    """Обработчик ошибки 404."""
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR.value)
def internal_error(error: Exception) -> Tuple[str, HTTPStatus]:
    """Обработчик ошибки 500."""
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error: InvalidAPIUsage) -> Tuple[Response, HTTPStatus]:
    """Обработчик исключения InvalidAPIUsage (для API)."""
    return jsonify(error.to_dict()), error.status_code
