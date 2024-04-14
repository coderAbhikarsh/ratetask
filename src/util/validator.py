from jsonschema import validate


class Validator:

    def __init__(self, request_params):
        self.request_params = request_params
        self.schema = {
            "type": "object",
            "properties": {
                "date_from": {"type": "string", "format": "%Y-%m-%d"},
                "date_to": {"type": "string", "format": "%Y-%m-%d"},
                "origin": {"type": "string"},
                "destination": {"type": "string"}
            },
            "required": ["date_from", "date_to", "origin", "destination"]
        }

    def validate_input(self):
        validate(self.request_params, self.schema)
