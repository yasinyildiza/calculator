"""Application exceptions."""

import abc


class BaseError(Exception, abc.ABC):
    """Base Exception class."""

    @property
    @abc.abstractmethod
    def key(self) -> str:
        """Return error key."""

    @property
    @abc.abstractmethod
    def status_code(self) -> int:
        """Return HTTP status error code; i.e., 4xx or 5xx."""


class ValidationError(BaseError):
    """Invalid input error, returns 400 BAD REQUEST."""

    key = "calculator.error.validation"
    status_code = 400
