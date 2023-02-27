"""Alternative HTTP interface for calculator in a more generic way."""

import flask

from calculator.core.schema import require_schema
from calculator.domain.calculator.models import Operands
from calculator.domain.calculator.models import Operation
from calculator.domain.calculator.registry import OperatorRegistry

bp = flask.Blueprint("calculator_v2", __name__)


@bp.route("/<operation_name>", methods=["POST"])
@require_schema(json="operands")
def compute(operation_name: str, operands: Operands) -> Operation:
    """Compute the result of the operation for the given operands."""
    return flask.jsonify(
        OperatorRegistry()[operation_name](
            left=operands.left,
            right=operands.right,
        )
        .run()
        .dict()
    )
