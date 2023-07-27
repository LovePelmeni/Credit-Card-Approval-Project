from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError 
from fastapi import Request 

def validation_exception_handler(request: Request, exc: RequestValidationError):

    errors = []
    for error in exc.errors():
        errors.append({'error': error['msg'], 'fields': error['loc'][1:]})
        
    return JSONResponse(
        status_code=400,
        content=errors
    )