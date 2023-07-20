from sqlalchemy import Column, Integer, Boolean, Float
from sqlalchemy.orm import declarative_base

Model = declarative_base()
class CreditTransaction(Model):

    __tablename__ = "CreditTransactions"

    ID = Column(Integer, unique=True, primary_key=True, index=True, nullable=False)
    customer_id = Column(Integer, unique=True, primary_key=True)
    bad = Column(Boolean, default=False)

class CustomerApplication(Model):

    __tablename__ = "CustomerApplications"

    ID = Column(Integer, unique=True, primary_key=True, index=True, nullable=False)
    email = Column(Integer, unique=True, nullable=False)
    annual_income = Column(Float, nullable=False)
    total_children = Column(Integer, nullable=True)
    age = Column(Integer, nullable=False)
    has_realty = Column(Boolean, default=False)
    has_car = Column(Boolean, default=False)
    has_mobile_phone = Column(Boolean, default=False)

