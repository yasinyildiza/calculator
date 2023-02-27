import argparse
import logging

import calculator

logger = logging.getLogger(__name__)


def run_local_server():
    app = calculator.create_app()
    app.run(debug=True, port=5000, threaded=False)  # nosec


if __name__ == "__main__":
    command_map = {
        "runserver": run_local_server,
    }
    parser = argparse.ArgumentParser(
        prog="manage.py",
        description="This is the main entrypoint to the service",
    )
    parser.add_argument(
        "command",
        type=str,
        choices=command_map.keys(),
        help="what command would you like to run?",
    )
    args = parser.parse_args()
    command_map[args.command]()
