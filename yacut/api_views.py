import re
from http import HTTPStatus
from typing import Any, Tuple

from flask import Response, jsonify, request, url_for

from settings import ORIGINAL_LINK_LENGTH, SHORT_LINK_LENGTH
from yacut import app, db
from yacut.constants import ORIGINAL_LINK_REGEX, SHORT_LINK_REGEX
from yacut.exceptions import AttemtsExceedingException, InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


class ErrorMessages:
    """Сообщения об ошибках для API."""
    INCORRECT_URL = 'В поле url передан некорректный URL.'
    INCORRECT_SHORT_ID = 'Указано недопустимое имя для короткой ссылки'
    INCORRECT_TYPE = 'В поле {field} должна быть передана строка'
    DUPLICATE_ID = 'Имя "{id}" уже занято.'
    URL_MISSING = '"url" является обязательным полем!'
    NOT_FOUND = 'Указанный id не найден'
    NO_DATA = 'Отсутствует тело запроса'
    ID_AUTOCREATE_ERROR = (
        'Не удалось создать короткую ссылку. Повторите попытку.'
    )


def validate_url(url: Any) -> None:
    """Валидация исходной (длинной) ссылки."""
    if url is None:
        raise InvalidAPIUsage(ErrorMessages.URL_MISSING)
    if not isinstance(url, str):
        raise InvalidAPIUsage(
            ErrorMessages.INCORRECT_TYPE.format(field='url')
        )
    if (
        len(url) > ORIGINAL_LINK_LENGTH or
        re.fullmatch(ORIGINAL_LINK_REGEX, url) is None
    ):
        raise InvalidAPIUsage(ErrorMessages.INCORRECT_URL)


def validate_custom_id(custom_id: Any) -> None:
    """Валидация id для короткой ссылки."""
    if not isinstance(custom_id, str):
        raise InvalidAPIUsage(
            ErrorMessages.INCORRECT_TYPE.format(field='custom_id')
        )
    if (
        len(custom_id) > SHORT_LINK_LENGTH or
        re.fullmatch(SHORT_LINK_REGEX, custom_id) is None
    ):
        raise InvalidAPIUsage(ErrorMessages.INCORRECT_SHORT_ID)
    if URLMap.query.filter_by(short=custom_id).first():
        raise InvalidAPIUsage(ErrorMessages.DUPLICATE_ID.format(id=custom_id))


@app.route('/api/id/', methods=('POST',))
def create_id() -> Tuple[Response, HTTPStatus]:
    """Запрос на создание короткой ссылки."""
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(ErrorMessages.NO_DATA)
    url = data.get('url')
    custom_id = data.get('custom_id')
    validate_url(url)
    if custom_id is None or custom_id == '':
        try:
            custom_id = get_unique_short_id()
        except AttemtsExceedingException as err:
            app.logger.error(err)
            raise InvalidAPIUsage(
                ErrorMessages.ID_AUTOCREATE_ERROR,
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )
    else:
        validate_custom_id(custom_id)
    url_map = URLMap(
        original=url,
        short=custom_id
    )
    db.session.add(url_map)
    db.session.commit()
    short_link = url_for(
        'redirect_url', short_id=url_map.short, _external=True
    )
    return (
        jsonify(url=url_map.original, short_link=short_link),
        HTTPStatus.CREATED
    )


@app.route('/api/id/<short_id>/', methods=('GET',))
def get_url(short_id: str) -> Tuple[Response, HTTPStatus]:
    """Запрос на получение ориганльной ссылки по короткому идентификатору."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage(
            ErrorMessages.NOT_FOUND,
            status_code=HTTPStatus.NOT_FOUND
        )
    return jsonify(url=url_map.original), HTTPStatus.OK
