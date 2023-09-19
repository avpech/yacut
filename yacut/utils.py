import random
import string

from settings import AUTO_ID_LENGTH, CREATE_ID_ATTEMPTS
from yacut.exceptions import AttemtsExceedingException
from yacut.models import URLMap


def get_unique_short_id() -> str:
    """Генерация случайного id для короткой ссылки.

    При превышении допустимого числа попыток автогенерации
    выбрасывает исключение AttemtsExceedingException.
    """
    chars = string.ascii_letters + string.digits
    new_id = ''.join(random.choice(chars) for _ in range(AUTO_ID_LENGTH))
    attempts = 0
    while URLMap.query.filter_by(short=new_id).first():
        new_id = ''.join(random.choice(chars) for _ in range(AUTO_ID_LENGTH))
        attempts += 1
        if attempts >= CREATE_ID_ATTEMPTS:
            raise AttemtsExceedingException(
                'Превышен лимит попыток для создания короткой ссылки'
            )
    return new_id
