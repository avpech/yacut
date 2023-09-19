####  Спринт 21 -  YaCut
---
### Описание
YaCut - сервис для укорачивания ссылок.
Ключевые возможности сервиса:
- генерация коротких ссылок и связь их с исходными длинными ссылками,
- переадресация на исходный адрес при обращении к коротким ссылкам.

### Стек технологий использованный в проекте:
- Python 3.7
- Flask
- SQLAlchemy
- Alembic
- WTForms

### Локальная установка и запуск сервиса
- Клонировать репозиторий и перейти в него в командной строке.
- Установить и активировать виртуальное окружение c учетом версии Python 3.7 (выбираем python не ниже 3.7):

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```
- Установить все зависимости из файла requirements.txt

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

- В корне проекта создать файл .env со следующими переменными

```bash
DATABASE_URI=<путь к базе данных в формате dialect+driver://username:password@host:port/database>
SECRET_KEY=<набор произвольных символов>
```
Примечание: если не указать DATABASE_URI, то будет использовано зачение по умолчанию sqlite:///db.sqlite3

- В корне проекта создать файл .flaskenv со следующими переменными

```bash
FLASK_APP=yacut
FLASK_ENV=development
```

- Выполнить миграции

```bash
flask db init
flask db migrate -m "initial"
flask db upgrade
```

- Запустить сервис

```bash
flask run
```
Сервис будет доступен по адресу http://localhost:5000
### API сервиса
Поддерживаются два эндпоинта:
- /api/id/ — POST-запрос на создание новой короткой ссылки;
- /api/id/<short_id>/ — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору.

Примеры запросов к API, варианты ответов и ошибок приведены в спецификации openapi.yml


##### Об авторе
Артур Печенюк
- :white_check_mark: [avpech](https://github.com/avpech)