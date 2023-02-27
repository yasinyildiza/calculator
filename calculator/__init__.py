"""Flask app entrypoint."""

import logging.config

import flask

from calculator.api.v1 import calculator as calculator_v1
from calculator.api.v2 import calculator as calculator_v2
from calculator.core import exceptions
from calculator.core import response
from calculator.core import schema


def setup_logging():
    """Configure logging once and for all."""
    logging.config.dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": (
                        "%(asctime)s | "
                        "%(process)d | "
                        "%(levelname)s | "
                        "%(pathname)s | "
                        "%(funcName)s | "
                        "%(lineno)d | "
                        "%(message)s"
                    )
                },
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "default",
                }
            },
            "root": {
                "level": "DEBUG",
                "handlers": ["default"],
            },
        }
    )


def setup_config(app: flask.Flask, config_override=None):
    """Initialize Flask app config."""
    app.config.from_object(__name__)
    app.config.update(config_override or {})


def setup_health_check(app: flask.Flask):
    """Add basic health check endpoint."""

    @app.route("/status")
    def health_check():
        return flask.jsonify({"success": True})


def setup_handlers(app: flask.Flask):
    """Register Flask error handlers."""

    @app.errorhandler(schema.SchemaValidationError)
    def schema_validation_error(exc):
        return (
            flask.jsonify(
                response.ErrorResponse(
                    key=exceptions.ValidationError.key, message=str(exc)
                ).dict()
            ),
            exceptions.ValidationError.status_code,
        )


def setup_blueprints(app: flask.Flask):
    """Register all Flask blueprints."""
    app.register_blueprint(calculator_v1.bp, url_prefix="/api/v1/calculator")
    app.register_blueprint(calculator_v2.bp, url_prefix="/api/v2/calculator")


def create_app(config_override=None):
    """Create Flask application."""
    app = flask.Flask(__name__)

    setup_logging()
    setup_config(app, config_override=config_override)
    setup_health_check(app)
    setup_handlers(app)
    setup_blueprints(app)

    return app
