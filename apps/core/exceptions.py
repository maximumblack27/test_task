class OrmValidationError(Exception):
    DEFAULT_MESSAGE = 'Ошибка валидации'

    def __init__(self, msg, index=None):
        self.msg = msg or self.DEFAULT_MESSAGE
