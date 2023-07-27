try:
    import fastapi
    import os
    import logging
    from fastapi.middleware.cors import CORSMiddleware

except (ImportError, ModuleNotFoundError):
    raise SystemExit("Failed to import critical startup modules, make sure they are installed.")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*")

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler(filename='./logs/startup.log')
logger.addHandler(file_handler)

try:
    import rest_controllers
    import exc_handlers 
    import py_logging
except (ImportError, ModuleNotFoundError) as imp_err:
    logger.critical({
        "name": imp_err.name
    })
    raise SystemExit("Failed to import local packages, check logs for more info")

DEBUG_MODE = os.environ.get("DEBUG_MODE", True)
APPLICATION_HOST = os.environ.get("APPLICATION_HOST", "localhost")
APPLICATION_PORT = int(os.environ.get("APPLICATION_PORT", "8080"))


try:
    py_logging.setup_logging() 
    application = fastapi.FastAPI(debug=DEBUG_MODE)

    application.add_api_route(
        methods=['POST'],
        path="/predict/card/approval/",
        endpoint=rest_controllers.predict_card_approval,
        response_description="Predicted Card Approval Status"
    )

    application.add_api_route(
        methods=["GET"],
        path="/healthcheck/",
        endpoint=rest_controllers.healthcheck,
        response_description="Healthcheck Endpoint for Application State Check"
    )

    application.add_exception_handler(
        exc_class_or_status_code=fastapi.exceptions.RequestValidationError,
        handler=exc_handlers.validation_exception_handler
    )

    application.add_middleware(
        middleware_class=CORSMiddleware,
        allow_credentials=True,
        allow_headers="*",
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_origins=ALLOWED_HOSTS,
    )

except (AttributeError, ValueError, fastapi.exceptions.FastAPIError, ModuleNotFoundError) as exc:
    logger.critical(exc_info={
        'name': exc.name,
        'type': exc.obj,
    }, msg="Startup Failure")
    raise SystemExit("Failed to start ASGI Server, check logs for more information")
