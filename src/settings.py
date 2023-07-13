import fastapi, os, uvicorn
from . import rest_controllers

DEBUG_MODE = os.environ.get("DEBUG_MODE", True)
APPLICATION_HOST = os.environ.get("APPLICATION_HOST", "localhost")
APPLICATION_PORT = int(os.environ.get("APPLICATION_PORT", "8080"))

application = fastapi.FastAPI(debug=DEBUG_MODE)
application.add_api_route(
    path="/predict/card/approval/",
    endpoint=rest_controllers.predict_card_approval,
    response_description="Predicted Card Approval Status"
)