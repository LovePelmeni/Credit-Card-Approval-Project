from db_settings import Model 
from sqlalchemy import Column, Integer, Boolean, Float

class CreditTransaction(Model):

    __tablename__ = "CreditTransactions"

    Id: Column(Integer, unique=True, primary_key=True)
    customer_id: Column(Integer, unique=True, primary_key=True)
    bad: Column(Boolean, default=False)

class CustomerApplication(Model):

    __tablename__ = "CustomerApplications"

    Id: Column(Integer, unique=True, primary_key=True)
    email: Column(Integer, unique=True, nullable=False)
    annual_income: Column(Float, nullable=False)
    total_children: Column(Integer, nullable=True)
    age: Column(Integer, nullable=False)
    has_realty: Column(Boolean, default=False)
    has_car: Column(Boolean, default=False)
    has_mobile_phone: Column(Boolean, default=False)
    
