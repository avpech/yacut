import random

from yacut.constants import CHARS
from yacut.exceptions import AttemtsExceedingException
from yacut.models import URLMap
from yacut.settings import AUTO_ID_LENGTH, CREATE_ID_ATTEMPTS


def get_unique_short_id() -> str:
    """Генерация случайного id для короткой ссылки.

    При превышении допустимого числа попыток автогенерации
    выбрасывает исключение AttemtsExceedingException.
    """
    new_id = ''.join(random.choice(CHARS) for _ in range(AUTO_ID_LENGTH))
    attempts = 0
    while URLMap.query.filter_by(short=new_id).first():
        new_id = ''.join(random.choice(CHARS) for _ in range(AUTO_ID_LENGTH))
        attempts += 1
        if attempts >= CREATE_ID_ATTEMPTS:
            raise AttemtsExceedingException(
                'Превышен лимит попыток для создания короткой ссылки'
            )
    return new_id
