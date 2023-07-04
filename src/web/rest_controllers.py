from settings import application
import typing, logging 
from rest_data_models import CardPredictionModel
import exceptions
import fastapi.responses
import pandas
from ..database import database_exceptions, connection

logger = logging.getLogger(__name__)

@application.get("/get/customer/credit/history/")
def check_client_credit_history(client_id: int):
    """
    Function that checks for customer credit history 
    If not exist, return 'Good Client' by default
    
    Args:
        Customer_Id: Unique Identifier of the customer 
    
    Returns:
        Client Status: 1 - Good Client, 0 - Bad Client (default 1)
        fastapi.responses.Response Object with Client Status
    """
    try:
        response = fastapi.responses.JSONResponse(status_code=201, content={'client_status': 1})
        client_status_query = connection.SQLConnection.execute(
            """
            select history_status from CustomerCreditHistory
            where customer_id = %s
            """ % client_id
        )
        if client_status_query:
            if client_status_query['history_status'] == "bad":
                response.context['client_status'] = 0
        return response
    except(database_exceptions.ConnectionError):
        logger.error("Failed to connect to database, error occured")
        raise exceptions.ClientCreditHistoryFailed()

@application.post("/predict/card/approval/")
def predict_card_approval(application_data: CardPredictionModel):
    """
    Function predicts whether client would be allowed to take 
    """
    try:
        data = application_data.to_dict()
        dataframe_data = pandas.DataFrame(data, columns=data.keys())
        prepared_dataset = prepare_dataset(dataframe_data)

        predicted_data = CreditCardApprover.predict_approval(prepared_dataset)

        return fastapi.responses.JSONResponse(
            status_code=201,
            content={
                "approved": predicted_data["approved"],
                "bank_name": predicted_data["bank_name"],
            }
        )

    except(exceptions.PredictionFailed) as prediction_err:
        logger.error("Failed to predict application allowance for credit card approval")
        raise prediction_err