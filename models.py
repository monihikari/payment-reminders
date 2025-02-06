from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base


class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    whatsapp = Column(String)
    

class Subscription(Base):
    __tablename__ = "subscription"

    subscription_id = Column(Integer, primary_key=True, index=True)
    amount = Column(String)
    status = Column(String)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    due_date = Column(DateTime)
