from starlette import status

class BaseError(Exception):
    def __init__(
            self,
            message='Произошла неизвестная ошибка.',
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ) -> None:
        self.status_code = status_code
        self.message = message
    
    def __str__(self) -> str:
        return self.message

class InvalidCredentialsError(BaseError):
    def __init__(self,
                 message: str='Неверный логин или пароль.',
                 status_code = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status_code)