import json

from src.config.configuration import Configuration
from src.util.validator import Validator
from src.service.rates_service import RatesService
from flask import Flask, Response, request
import atexit

app = Flask(__name__)

config = Configuration()
container = config.build_postgres_image()
db_session = config.connect_to_postgres()


def exit_handler():
    """
    This method is called when the application is shutting down
    to perform any close up actions like closing database connection
    or stopping container
    """
    print("Performing final cleanup action")
    print("Closing db session")
    db_session.close()
    print("Stopping and removing container")
    container.stop()
    container.remove()


atexit.register(exit_handler)


@app.route("/rates", methods=["GET"])
def get_rates():
    try:
        validator = Validator(request.args)
        validator.validate_input()

        rate_service = RatesService(db_session)
        rates = rate_service.get_rates(**request.args)

        return Response(json.dumps(rates), status=200, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"msg": "Error occurred while fetching rates : {}".format(e)}),
                        status=500, mimetype='application/json')


if __name__ == "__main__":
    app.run()
