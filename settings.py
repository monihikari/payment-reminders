import os

from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

WHASTAPP_ACCESS_TOKEN = os.environ.get("WHASTAPP_ACCESS_TOKEN")
WHASTAPP_PHONE_ID = os.environ.get("WHASTAPP_PHONE_ID")
DATABASE_URL = os.environ.get("DATABASE_URL")


def build_supabase_client() -> Client:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    return  create_client(url, key)
    