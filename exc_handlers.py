from fastapi import exceptions 


def invalid_form_handler(*args, **kwargs): 
    return exceptions.HTTPException(status_code=400, 
                                    detail="Invalid Form, make sure your form has correct values and all fields are filled up")
