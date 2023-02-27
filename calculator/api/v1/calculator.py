"""HTTP interface for calculator."""

import flask

from calculator.core.schema import require_schema
from calculator.domain.calculator.models import Operands
from calculator.domain.calculator.models import Operation
from calculator.domain.calculator.operators.addition import Addition
from calculator.domain.calculator.operators.division import Division
from calculator.domain.calculator.operators.multiplication import Multiplication
from calculator.domain.calculator.operators.subtraction import Subtraction

bp = flask.Blueprint("calculator_v1", __name__)


@bp.route("/addition", methods=["POST"])
@require_schema(json="operands")
def add(operands: Operands) -> Operation:
    """Add two operands to each other, and return the resultant operation."""
    return flask.jsonify(
        Addition(left=operands.left, right=operands.right).run().dict()
    )


@bp.route("/subtraction", methods=["POST"])
@require_schema(json="operands")
def subtract(operands: Operands) -> Operation:
    """Subtract right operand from the left, and return the resultant operation."""
    return flask.jsonify(
        Subtraction(left=operands.left, right=operands.right).run().dict()
    )


@bp.route("/multiplication", methods=["POST"])
@require_schema(json="operands")
def multiply(operands: Operands) -> Operation:
    """Multiple two operands, and return the resultant operation."""
    return flask.jsonify(
        Multiplication(left=operands.left, right=operands.right).run().dict()
    )


@bp.route("/division", methods=["POST"])
@require_schema(json="operands")
def divide(operands: Operands) -> Operation:
    """Divide left operand by the left, and return the resultant operation."""
    return flask.jsonify(
        Division(left=operands.left, right=operands.right).run().dict()
    )
