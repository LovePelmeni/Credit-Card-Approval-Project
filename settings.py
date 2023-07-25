try:
    import fastapi
    import os
    import logging
except (ImportError, ModuleNotFoundError) as im_err:
    raise SystemExit("Failed to import critical startup modules, make sure they are installed.")

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler(filename='./logs/startup.log')
logger.addHandler(file_handler)

try:
    import rest_controllers
    import exc_handlers 
except (ImportError, ModuleNotFoundError) as imp_err:
    logger.critical({
        "name": imp_err.name,
        "exc_msg": imp_err.msg
    })
    raise SystemExit("Failed to import local packages, check logs for more info")

DEBUG_MODE = os.environ.get("DEBUG_MODE", True)
APPLICATION_HOST = os.environ.get("APPLICATION_HOST", "localhost")
APPLICATION_PORT = int(os.environ.get("APPLICATION_PORT", "8080"))

try:
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

    application.add_exception_handler(
        exc_class_or_status_code=422,
        handler=exc_handlers.invalid_form_handler
    )
except (AttributeError, ValueError, fastapi.exceptions.FastAPIError, ModuleNotFoundError) as exc:
    logger.critical(exc_info={
        'name': exc.name,
        'type': exc.obj,
        'exc_msg': exc.msg
    }, msg="Startup Failure")
    raise SystemExit("Failed to start ASGI Server, check logs for more information")
