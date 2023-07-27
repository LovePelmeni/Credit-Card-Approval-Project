def create_emp_stability(number_of_years: int):
    """
    Function creates feature of employee stability, based on the number of years
    
    Args:
        number_of_years: int
    """
    return True if number_of_years >= 5 else False 

def create_owns_realty_and_car(has_car: bool, has_realty: bool):
    return has_car and has_realty 
    
def create_contact_information(has_phone_number: bool, has_email: bool):
    return has_phone_number or has_email
