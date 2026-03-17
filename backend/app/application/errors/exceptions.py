from typing import Any, Dict, Optional

class AppError(RuntimeError):
    """
    Base exception class for application errors.
    """

    def __init__(
        self,
        code: int,
        message: str,
        status_code: int = 400,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Initializes the AppError instance.

        Args:
            code (int): Error code.
            message (str): Error message.
            status_code (int, optional): HTTP status code. Defaults to 400.
            data (Optional[Any], optional): Additional data. Defaults to None.
            headers (Optional[Dict[str, str]], optional): Custom headers. Defaults to None.
        """
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.data = data
        self.headers = headers or {}


class NotFoundError(AppError):
    """
    Exception raised when a resource is not found.
    """

    def __init__(self, message: str = "Resource not found"):
        """
        Initializes the NotFoundError instance.

        Args:
            message (str, optional): Error message. Defaults to "Resource not found".
        """
        super().__init__(code=404, message=message, status_code=404)


class BadRequestError(AppError):
    """
    Exception raised when a bad request is made.
    """

    def __init__(self, message: str = "Bad request parameters"):
        """
        Initializes the BadRequestError instance.

        Args:
            message (str, optional): Error message. Defaults to "Bad request parameters".
        """
        super().__init__(code=400, message=message, status_code=400)


class ValidationError(AppError):
    """
    Exception raised when validation fails.
    """

    def __init__(self, message: str = "Validation error"):
        """
        Initializes the ValidationError instance.

        Args:
            message (str, optional): Error message. Defaults to "Validation error".
        """
        super().__init__(code=422, message=message, status_code=422)


class ServerError(AppError):
    """
    Exception raised when an internal server error occurs.
    """

    def __init__(self, message: str = "Internal server error"):
        """
        Initializes the ServerError instance.

        Args:
            message (str, optional): Error message. Defaults to "Internal server error".
        """
        super().__init__(code=500, message=message, status_code=500)


class UnauthorizedError(AppError):
    """
    Exception raised when authentication is required.
    """

    def __init__(
        self,
        message: str = "Authentication required",
        *,
        error_code: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Initializes the UnauthorizedError instance.

        Args:
            message (str, optional): Error message. Defaults to "Authentication required".
            error_code (Optional[str], optional): Custom error code. Defaults to None.
            headers (Optional[Dict[str, str]], optional): Custom headers. Defaults to None.
        """
        data = {"code": error_code} if error_code else None
        super().__init__(code=401, message=message, status_code=401, data=data, headers=headers)