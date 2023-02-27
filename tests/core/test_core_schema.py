import flask
import pytest

from calculator.core.schema import ArgsSchemaValidationError
from calculator.core.schema import JsonSchemaValidationError
from calculator.core.schema import require_schema


class ArgsSchema:
    exc = Exception("calculator.tests.flask.utils.schema.args.schema.error")

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if "exc" in self.kwargs:
            raise self.exc


class JsonSchema:
    exc = Exception("calculator.tests.flask.utils.schema.json.schema.error")

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if "exc" in self.kwargs:
            raise self.exc


def _create_flask_app():
    app = flask.Flask(__name__)
    app.config["TESTING"] = True

    @app.route("/no_schema", methods=["GET", "POST"])
    @require_schema()
    def ep_no_schema():
        return {"success": True}

    @app.route("/args_no_schema", methods=["GET"])
    @require_schema(args="query")
    def ep_args_no_schema(query):
        return {"query": query}

    @app.route("/args_schema", methods=["GET"])
    @require_schema(args="query")
    def ep_args_schema(query: ArgsSchema):
        return {"query": query.kwargs}

    @app.route("/json_no_schema", methods=["POST"])
    @require_schema(json="body")
    def ep_json_no_schema(body):
        return {"body": body}

    @app.route("/json_schema", methods=["POST"])
    @require_schema(json="body")
    def ep_json_schema(body: JsonSchema):
        return {"body": body.kwargs}

    @app.route("/mixed", methods=["POST"])
    @require_schema(args="query", json="body")
    def ep_mixed(query: ArgsSchema, body: JsonSchema):
        return {
            "query": query.kwargs,
            "body": body.kwargs,
        }

    return app


class TestFlaskUtilsSchema:
    @pytest.fixture
    def flask_app(self):
        app = _create_flask_app()
        yield app

    @pytest.fixture
    def test_client(self, flask_app):
        yield flask_app.test_client()

    @pytest.fixture
    def test_query(self):
        yield {
            "key1": "val1",
            "key2": "val2",
        }

    @pytest.fixture
    def test_body_dict(self):
        yield {
            "field1": "value1",
            "field2": "value2",
            "field3": "value3",
        }

    @pytest.fixture
    def test_body_list(self):
        yield [
            {
                "field11": "value11",
                "field12": "value12",
                "field13": "value13",
            },
            {
                "field21": "value21",
                "field22": "value22",
                "field23": "value23",
            },
            {
                "field31": "value31",
                "field32": "value32",
                "field33": "value33",
            },
        ]

    def test_no_schema(self, test_client):
        response = test_client.get("/no_schema")
        assert response.status_code == 200
        assert response.json == {"success": True}

    def test_args_no_schema(self, test_client, test_query):
        response = test_client.get("/args_no_schema", query_string=test_query)
        assert response.status_code == 200
        assert response.json == {"query": test_query}

    def test_args_schema_error(self, test_client):
        query = {"exc": "yes"}
        with pytest.raises(ArgsSchemaValidationError) as exc:
            test_client.get("/args_schema", query_string=query)

        exception = exc.value
        assert exception.component == "args"
        assert exception.schema == ArgsSchema
        assert exception.value == query
        assert exception.original_exception == ArgsSchema.exc

    def test_args_schema_success(self, test_client, test_query):
        response = test_client.get("/args_schema", query_string=test_query)
        assert response.status_code == 200
        assert response.json == {"query": test_query}

    def test_json_no_schema(self, test_client, test_body_dict):
        response = test_client.post("/json_no_schema", json=test_body_dict)
        assert response.status_code == 200
        assert response.json == {"body": test_body_dict}

    def test_json_schema_null_body(self, test_client):
        with pytest.raises(JsonSchemaValidationError) as exc:
            test_client.post("/json_schema")

        exception = exc.value
        assert exception.component == "json"
        assert exception.schema == JsonSchema
        assert exception.value is None
        assert isinstance(exception.original_exception, ValueError)

    def test_json_schema_not_dict(self, test_client, test_body_list):
        with pytest.raises(JsonSchemaValidationError) as exc:
            test_client.post("/json_schema", json=test_body_list)

        exception = exc.value
        assert exception.component == "json"
        assert exception.schema == JsonSchema
        assert exception.value == test_body_list
        assert isinstance(exception.original_exception, TypeError)

    def test_json_schema_error(self, test_client):
        body = {"exc": "yes"}
        with pytest.raises(JsonSchemaValidationError) as exc:
            test_client.post("/json_schema", json=body)

        exception = exc.value
        assert exception.component == "json"
        assert exception.schema == JsonSchema
        assert exception.value == body
        assert exception.original_exception == JsonSchema.exc

    def test_json_schema_success(self, test_client, test_body_dict):
        response = test_client.post("/json_schema", json=test_body_dict)
        assert response.status_code == 200
        assert response.json == {"body": test_body_dict}

    def test_mixed(self, test_client, test_query, test_body_dict):
        response = test_client.post(
            "/mixed",
            query_string=test_query,
            json=test_body_dict,
        )
        assert response.status_code == 200
        assert response.json == {
            "query": test_query,
            "body": test_body_dict,
        }
