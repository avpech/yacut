import string

CHARS = string.ascii_letters + string.digits

# Регулярное выражение, соответствующее URL-паттерну.
ORIGINAL_LINK_REGEX = (
    r"^[a-z]+://(?P<host>[^\/\?:]+)(?P<port>:[0-9]+)?"
    r"(?P<path>\/.*?)?(?P<query>\?.*)?$"
)

# Регулярное выражение, которому соответствует строка,
# состоящая из цифр, заглавных и строчных латинских букв.
SHORT_LINK_REGEX = r'^[a-zA-Z0-9]+$'
