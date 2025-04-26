import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("SUPABASE_DB"),
        user=os.getenv("SUPABASE_USER"),
        password=os.getenv("SUPABASE_PASSWORD"),
        host=os.getenv("SUPABASE_HOST"),
        port=os.getenv("SUPABASE_PORT"),
    )