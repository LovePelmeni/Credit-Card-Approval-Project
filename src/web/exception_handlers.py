from settings import application 
from fastapi.exception_handlers import http_exception_handler 
from exceptions import PredictionFailed 
import fastapi.responses 

@http_exception_handler(exc=PredictionFailed)
def prediction_failure_handler(request, exc):
    """
    Exception Handler for Prediction Card Approval Error Failure 
    """
    return fastapi.responses.Response(
        status_code=501,
        content={
            "error": "Failed to predict approval status, error on the server side occured"
        },
    )