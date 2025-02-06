import zoneinfo

from datetime import datetime
from fastapi import FastAPI
from settings import WHASTAPP_ACCESS_TOKEN, WHASTAPP_PHONE_ID, build_supabase_client
from supabase import Client
from dotenv import load_dotenv
from heyoo import WhatsApp


load_dotenv() # Load environment variables from the .env file
supabase: Client = build_supabase_client() # Import supabase configuratin

app = FastAPI()

@app.get("/")
async def root():
    response = supabase.table("customer").select("*").execute()

    print("")
    print(response)
    print("")

    return {"message": "Hola, Moni"}


def make_message(name: str, amount: str, expiration_date: str) -> str:
    return "Hola {name}, te recordamos que tu pago de: {amount} vence el {expiration_date}".format(
        name=name,
        amount=amount,
        expiration_date=expiration_date,
    )


@app.post("/send")
async def send():
    # .select("customer_id, name, SUBSCRIPTION(amount)")\
    response = supabase.table("customer").select("*, subscription(*)").execute()
    customers = response.data
    
    
    
    for customer in customers:
        
        amount = "0"
        due_date = ""
        # import ipdb; ipdb.set_trace()
           
        if customer["subscription"]:
            amount = customer["subscription"][0]["amount"]
            due_date =  customer["subscription"][0]["due_date"]
            
        mesagge = make_message(
            name=customer['name'],
            amount=amount,
            expiration_date=due_date,
        )

        mensajeWa=WhatsApp(WHASTAPP_ACCESS_TOKEN, WHASTAPP_PHONE_ID)
        mensajeWa.send_message(mesagge, customer['whatsapp'])
    
    return {"message": "mensaje enviado"}