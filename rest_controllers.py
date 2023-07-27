from src.modeling import modeling, feature_form, exceptions
import fastapi.responses
import fastapi.exceptions
import logging
import fastapi.requests
from fastapi.responses import Response

logger = logging.getLogger(__name__)
handler = logging.FileHandler(filename="./logs/rest_controllers.log")
logger.addHandler(handler)


def predict_card_approval(application_data: feature_form.CardApprovalFeatures) -> Response:
    """
    Function predicts whether client would be allowed to have a credit card or not 
    Args:
        application_data: Feature Dataset with client's personal informaton
    """
    try:
        predicted_status = modeling.prediction_model.predict_card_approval(application_data)
        return fastapi.responses.JSONResponse(
            status_code=201,
            content={
                "status": int(predicted_status)
            }
        )

    except (ValueError) as val_err:
        return fastapi.exceptions.HTTPException(
            status_code=400, detail=val_err.args)

    except (exceptions.PredictionFailed) as prediction_err:
        logger.error(prediction_err.msg)
        return fastapi.responses.JSONResponse(status_code=500,
                                              content={'error': 'server failed to predict status, internal error :('})


def healthcheck(request: fastapi.requests.Request):
    return fastapi.responses.Response(status_code=200)
