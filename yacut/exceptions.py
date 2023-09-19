from http import HTTPStatus
from typing import Dict, Optional


class AttemtsExceedingException(Exception):
    """Превышение допустимого числа попыток автогенерации id для ссылки."""
    pass


class InvalidAPIUsage(Exception):
    """Исключение для обработчика ошибок, возникающих при работе с API."""
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self,
                 message: str,
                 status_code: Optional[HTTPStatus] = None) -> None:
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self) -> Dict[str, str]:
        return dict(message=self.message)
