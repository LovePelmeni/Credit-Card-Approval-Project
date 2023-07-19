import fastapi, os
import rest_controllers
import logging 

logger = logging.getLogger(__name__)
logging.basicConfig(filename="startup.log")

DEBUG_MODE = os.environ.get("DEBUG_MODE", True)
APPLICATION_HOST = os.environ.get("APPLICATION_HOST", "localhost")
APPLICATION_PORT = int(os.environ.get("APPLICATION_PORT", "8080"))

application = fastapi.FastAPI(debug=DEBUG_MODE)
application.add_api_route(
    methods=['POST'],
    path="/predict/card/approval/",
    endpoint=rest_controllers.predict_card_approval,
    response_description="Predicted Card Approval Status"
)

application.add_api_route(
    methods=["GET"],
    path="/heatlhcheck/",
    endpoint=rest_controllers.healthcheck,
    response_description="Healthcheck Endpoint for Application State Check"
)