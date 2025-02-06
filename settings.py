import os
from supabase import create_client, Client

WHASTAPP_ACCESS_TOKEN = os.environ.get("WHASTAPP_ACCESS_TOKEN")
WHASTAPP_PHONE_ID = os.environ.get("WHASTAPP_PHONE_ID")


def build_supabase_client() -> Client:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    return  create_client(url, key)
    