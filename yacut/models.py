from datetime import datetime

from settings import ORIGINAL_LINK_LENGTH, SHORT_LINK_LENGTH
from yacut import db


class URLMap(db.Model):
    """Модель для сопоставления исходной ссылки и id для короткой ссылки."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_LINK_LENGTH), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
