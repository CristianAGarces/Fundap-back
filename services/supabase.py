from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# 🚨 Validación de variables de entorno
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ Variables de entorno SUPABASE_URL o SUPABASE_KEY no están definidas")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)