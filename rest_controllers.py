from src.modeling import modeling, feature_form, exceptions
import fastapi.responses
import fastapi.exceptions
import logging
import fastapi.requests

logger = logging.getLogger(__name__)

def predict_card_approval(application_data: feature_form.CardApprovalFeatures):
    """
    Function predicts whether client would be allowed to have a credit card or not 
    Args:
        application_data: Feature Dataset with client's personal informaton
    """
    try:
        predicted_status = modeling.prediction_model.predict_approval(application_data)
        return fastapi.responses.JSONResponse(
            status_code=201,
            content={
                "status": "Approved" if predicted_status == 1 else "Rejected",
            }
        )
    except(ValueError) as val_err:
        return fastapi.exceptions.HTTPException(
        status_code=400, detail=val_err.args)

    except(exceptions.PredictionFailed) as prediction_err:
        logger.error("""Failed to predict application
        allowance for credit card approval. [%s]""" % prediction_err)
        return fastapi.responses.Response(status_code=500, 
        content={'error': 'server failed to predict status, internal error :('})


def healthcheck(request: fastapi.requests.Request):
    return fastapi.responses.Response(status_code=200)