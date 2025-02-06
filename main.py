from datetime import datetime
from fastapi import FastAPI
from models import Customer, Subscription
from settings import WHASTAPP_ACCESS_TOKEN, WHASTAPP_PHONE_ID, build_supabase_client
from supabase import Client
from heyoo import WhatsApp
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from sqlalchemy import func


supabase: Client = build_supabase_client() # Import supabase configuratin
app = FastAPI()


@app.get("/")
async def root():
    response = supabase.table("customer").select("*").execute()

    print("")
    print(response)
    print("")

    return {"message": "Hola, yo"}


def make_message(name: str, amount: str, expiration_date: str) -> str:
    return "Hola {name}, te recordamos que tu pago de: {amount} vence el {expiration_date}".format(
        name=name,
        amount=amount,
        expiration_date=expiration_date,
    )


@app.post("/send")
async def send(db: Session = Depends(get_db)):
    # .select("customer_id, name, SUBSCRIPTION(amount)")\
    
    response = supabase.table("customer").select("*, subscription(*)").execute()
    customers = response.data
    
    # customers_items = db.query(Customer).all()
    customers_items = db.query(
        Customer.name,
        Customer.whatsapp,
        Subscription.amount,
        Subscription.status,
        Subscription.due_date
    ).join(
        Subscription, Customer.customer_id == Subscription.customer_id
    ).filter(
        func.extract('epoch', Subscription.due_date - func.current_date()) / 3600 <= 24
    ).all()
    
    print(customers) # Supabase
    print(customers_items) # SQLAlchemy
    
    # import ipdb; ipdb.set_trace()
    
    for customer in customers_items:
        
        # amount = "0"
        # due_date = ""
        # import ipdb; ipdb.set_trace()
           
        # if customer["subscription"]:
        #     amount = customer["subscription"][0]["amount"]
        #     due_date =  customer["subscription"][0]["due_date"]
        
            
        message = make_message(
            # name=customer['name'],
            # amount=amount,
            # expiration_date=due_date,
            name=customer[0],
            amount=customer[2],
            expiration_date=str(customer[4]),
        )

        whatsapp_message = WhatsApp(WHASTAPP_ACCESS_TOKEN, WHASTAPP_PHONE_ID)
        whatsapp_message.send_message(message, customer['whatsapp'])
    
    return {"message": "Mensaje enviado"}