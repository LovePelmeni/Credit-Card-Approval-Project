from sqlalchemy import Column, Integer, Boolean, String, Enum
from sqlalchemy.orm import declarative_base
import enum

Model = declarative_base()
class CodeGender(enum.Enum):
    """
    Enum Class represents gender choice 
    F - Female 
    M - Male
    """
    Male = "M" # denotes as Male
    Female = "F" # denotes as Female
class IncomeCategory(enum.Enum):
    """
    Enum Class reprensents income category of the client 
    """
    Student = "Student"
    Pensioner = "Pensioner"
    Working = "Working"
    CommAssociate = "Commercial associate"
    StateServant = "State servant"

class EducationCategory(enum.Enum):
    """
    Enum class represents education category of the client
    """
    acad_educ = 'Academic degree'
    higher_educ = 'Higher education'
    incomp_higher_educ = 'Incomplete higher'
    secondary_educ = 'Secondary / secondary special'
    lower_educ = 'Lower secondary'

class LivingPlace(enum.Enum):
    """
    Enum class represents type of living place of the client
    """
    co_op_apartment = 'Co-op apartment',
    office_apartment = 'Office apartment',
    municipal_apartment = 'Municipal apartment',
    house_apartment = 'House / apartment',
    rented_apartment = 'Rented apartment', 
    with_parents = 'With parents',
class CreditTransaction(Model):

    __tablename__ = "transactions"
    transaction_id = Column(Integer, unique=True, primary_key=True)
    ID = Column(Integer, unique=True, nullable=False, index=True)
    STATUS = Column(String, unique=True, nullable=False)
    MONTHS_BALANCE = Column(Integer, unique=True)
class CustomerApplication(Model):

    __tablename__ = "applications"

    ID = Column(Integer, unique=True, primary_key=True, index=True, nullable=False)
    CODE_GENDER = Column(Enum(CodeGender), nullable=False)
    FLAG_OWN_CAR = Column(Boolean, default=False)
    FLAG_OWN_REALTY = Column(Boolean, default=False)
    CNT_CHILDREN = Column(Integer, nullable=False)
    AMT_INCOME_TOTAL = Column(Boolean, default=False)
    NAME_INCOME_TYPE = Column(Enum(IncomeCategory), default=False)
    NAME_EDUCATION_TYPE = Column(Enum(EducationCategory), default=False)
    NAME_FAMILY_STATUS = Column(String, nullable=False)
    NAME_HOUSING_TYPE = Column(Enum(LivingPlace), nullable=False)
    
    DAYS_BIRTH = Column(Integer, default=True)
    FLAG_MOBIL = Column(Boolean, default=False)
    FLAG_PHONE = Column(Boolean, default=False)
    FLAG_WORK_PHONE = Column(Boolean, default=False)
    FLAG_EMAIL = Column(Boolean, default=False)
    CNT_FAM_MEMBERS = Column(Integer, nullable=False)
    OCCUPATION_TYPE = Column(String, nullable=False)
    DAYS_EMPLOYED = Column(String, nullable=False)



