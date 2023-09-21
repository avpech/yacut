from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from yacut.constants import SHORT_LINK_REGEX
from yacut.settings import ORIGINAL_LINK_LENGTH, SHORT_LINK_LENGTH


class URLMapForm(FlaskForm):
    """Форма для главной страницы."""
    original_link = URLField(
        'Длинная ссылка',
        validators=(
            DataRequired(message='Обязательное поле'),
            Length(max=ORIGINAL_LINK_LENGTH),
            URL(message='Некорректный URL')
        )
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=(
            Optional(),
            Length(max=SHORT_LINK_LENGTH),
            Regexp(
                SHORT_LINK_REGEX,
                message=('Использованы недопустимые символы. '
                         'Допускается использование цифр и латинских букв.')
            )
        )
    )
    submit = SubmitField('Создать')
