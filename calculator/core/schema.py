"""Request input (query/body) validator based on type hints.

Example usage (query validation)
-------------
class MyQuery(pydantic.BaseModel):
    x: int
    y: str


@app.route("/path")
@schema.require_schema(args="query")
def add(query: MyQuery):
    return jsonify(
        {
            "result": query.x + query.y
        }
    )


Example usage (body validation)
-------------
class MyBody(pydantic.BaseModel):
    x: int
    y: str


@app.route("/path")
@schema.require_schema(json="body")
def add(body: MyBody):
    return jsonify(
        {
            "result": body.x + body.y
        }
    )


Exceptions raised during validation can be captured at Flask app/blueprint level

@app.errorhandler(schema.SchemaValidationError)
def schema_validation_error(exc):
    return jsonify(
        {
            "error": str(exc),
            "details": {
                "schema": exc.schema,
                "value": exc.value,
                "original_exception": exc.original_exception,
            },
        }
    )
"""

import functools
import typing

import flask


class SchemaValidationError(Exception):
    """Base exception for schema validation errors.

    Attributes:
        schema: pydantic model of either args (query) or json (body) schema
        value: the input value (query or body) that is not valid in the given schema
        original_exception: the original exception raised during the validation
    """

    component: str = ""

    def __init__(
        self,
        schema: typing.Type,
        value: typing.Any,
        original_exception: Exception,
    ):
        self.schema = schema
        self.value = value
        self.original_exception = original_exception

        super().__init__(
            f'"{self.component}" schema validation error: {self.original_exception}'
        )


class ArgsSchemaValidationError(SchemaValidationError):
    """Request query is not valid."""

    component: str = "args"


class JsonSchemaValidationError(SchemaValidationError):
    """Request body is not valid."""

    component: str = "json"


def process_args(args: str, func: typing.Callable) -> typing.Dict[str, dict]:
    """Build kwargs for view function from flask.request.args.

    Args:
        args: name of the argument in the view function for flask.request.args

    Returns:
        dict[str, dict]
    """
    args_schema = func.__annotations__.get(args)
    args_value = flask.request.args.to_dict()
    if args_schema:
        try:
            args_obj = args_schema(**args_value)
        except Exception as exc:
            raise ArgsSchemaValidationError(
                schema=args_schema,
                value=args_value,
                original_exception=exc,
            ) from exc

        return {args: args_obj}

    return {args: args_value}


def process_json(json: str, func: typing.Callable) -> typing.Dict[str, dict]:
    """Build kwargs for view function from flask.request.get_json.

    Args:
        json: name of the argument in the view function for flask.request.get_json

    Returns:
        dict[str, dict]
    """
    json_schema = func.__annotations__.get(json)
    json_value = flask.request.get_json(force=False, silent=True)
    if json_schema:
        if json_value is None:
            raise JsonSchemaValidationError(
                schema=json_schema,
                value=json_value,
                original_exception=ValueError("request body must not be None"),
            )

        if not isinstance(json_value, dict):
            raise JsonSchemaValidationError(
                schema=json_schema,
                value=json_value,
                original_exception=TypeError("request body must be a dict"),
            )

        try:
            json_obj = json_schema(**json_value)
        except Exception as exc:
            raise JsonSchemaValidationError(
                schema=json_schema,
                value=json_value,
                original_exception=exc,
            ) from exc

        return {json: json_obj}

    return {json: json_value}


def require_schema(
    args: typing.Optional[str] = None,
    json: typing.Optional[str] = None,
) -> typing.Callable:
    """Decorate flask views to enforce schema for request.args and/or request.get_json.

    The decorator reads the argument name for `args`, and then extracts the type hint
    of that argument from the (decorated) view function's signature.
    The constructor of that type is called with `flask.request.args.to_dict()`
    as named arguments; i.e., Schema(**flask.request.args.to_dict())

    Similarly, the decorator reads the argument name for `json`, and then extracts the
    type hint of that argument from the (decorated) view function's signature.
    The constructor of that type is called with `flask.request.get_json()`
    as named arguments; i.e., Schema(**flask.request.get_json())

    Args:
        args: name of the argument in the view function for flask.request.args
        json: name of the argument in the view function for flask.request.get_json

    Returns:
        Callable: decorated view function
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*func_args, **func_kwargs):
            if args is not None:
                func_kwargs.update(process_args(args=args, func=func))

            if json is not None:
                func_kwargs.update(process_json(json=json, func=func))

            return func(*func_args, **func_kwargs)

        return wrapper

    return decorator
