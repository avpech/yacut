import os


class Config(object):
    """Класс конфигурации приложения."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


AUTO_ID_LENGTH = 6  # длина id короткой ссылки при автоматической генерации
CREATE_ID_ATTEMPTS = 100  # количество попыток автосоздания id короткой ссылки
ORIGINAL_LINK_LENGTH = 256  # максимальная длина оригинальной ссылки
SHORT_LINK_LENGTH = 16  # максимальная длина id короткой ссылки
