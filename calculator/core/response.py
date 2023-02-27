"""Application error response structure."""

import pydantic


class ErrorResponse(pydantic.BaseModel):
    """Error Response data model for Flask views."""

    key: str
    message: str
