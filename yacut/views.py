from flask import flash, redirect, render_template, url_for
from werkzeug import wrappers

from yacut import app, db
from yacut.exceptions import AttemtsExceedingException
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


class FlashMessages:
    """Сообщения для функции flash."""
    DUPLICATE_ID = 'Имя {id} уже занято!'
    ID_AUTOCREATE_ERROR = (
        'Не удалось создать короткую ссылку. Повторите попытку.'
    )


@app.route('/', methods=('GET', 'POST'))
def index() -> str:
    """Функция представления для главной страницы."""
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id = form.custom_id.data
    if custom_id and URLMap.query.filter_by(short=custom_id).first():
        flash(FlashMessages.DUPLICATE_ID.format(id=custom_id))
        return render_template('index.html', form=form)
    if not custom_id or custom_id.isspace():
        try:
            custom_id = get_unique_short_id()
        except AttemtsExceedingException as err:
            flash(FlashMessages.ID_AUTOCREATE_ERROR)
            app.logger.error(err)
            return render_template('index.html', form=form)
    url_map = URLMap(
        original=form.original_link.data,
        short=custom_id
    )
    db.session.add(url_map)
    db.session.commit()
    short_link = url_for(
        'redirect_url', short_id=url_map.short, _external=True
    )
    return render_template('index.html', form=form, short_link=short_link)


@app.route('/<short_id>', methods=('GET',))
def redirect_url(short_id: str) -> wrappers.Response:
    """Функция представления для переадресации по короткой ссылке."""
    link = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(link.original)
