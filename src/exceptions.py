class CustomError(Exception):
    pass


class DBError(CustomError):
    pass


class LLMError(CustomError):
    pass
