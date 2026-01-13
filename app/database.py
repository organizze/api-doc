from supabase import create_client, Client
from app.config import settings


def get_supabase_client() -> Client:
    """Retorna cliente Supabase configurado"""
    return create_client(settings.supabase_url, settings.supabase_key)


# Cliente singleton para uso geral
supabase: Client = get_supabase_client()
