from sqlalchemy import Column, Integer, Boolean, Float, String
from sqlalchemy.orm import declarative_base

Model = declarative_base()
class CreditTransaction(Model):

    __tablename__ = "transactions"
    transaction_id = Column(Integer, unique=True, primary_key=True)
    ID = Column(Integer, unique=True, nullable=False, index=True)
    STATUS = Column(String, unique=True, nullable=False)
    MONTHS_BALANCE = Column(Integer, unique=True)
class CustomerApplication(Model):

    __tablename__ = "applications"

    ID = Column(Integer, unique=True, primary_key=True, index=True, nullable=False)
    CODE_GENDER = Column(Integer, unique=True, nullable=False)
    FLAG_OWN_CAR = Column(Float, nullable=False)
    FLAG_OWN_REALTY = Column(Integer, nullable=True)
    CNT_CHILDREN = Column(Integer, nullable=False)
    AMT_INCOME_TOTAL = Column(Boolean, default=False)
    NAME_INCOME_TYPE = Column(Boolean, default=False)
    NAME_EDUCATION_TYPE = Column(Boolean, default=False)
    NAME_FAMILY_STATUS = Column(String, nullable=False)
    NAME_HOUSING_TYPE = Column(String, nullable=False)
    
    DAYS_BIRTH = Column(Integer, default=True)
    FLAG_MOBIL = Column(Boolean, default=False)
    FLAG_PHONE = Column(Boolean, default=False)
    FLAG_WORK_PHONE = Column(Boolean, default=False)
    FLAG_EMAIL = Column(Boolean, default=False)
    CNT_FAM_MEMBERS = Column(Integer, nullable=False)
    OCCUPATION_TYPE = Column(String, nullable=False)
    DAYS_EMPLOYED = Column(String, nullable=False)



