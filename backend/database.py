import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


load_dotenv()

def get_db():
    connection_string = os.getenv("SUPABASE_CONNECTION_STRING")
        
        
    parsed = urlparse(connection_string)
        
    return psycopg2.connect(
        
        
        # Extract components
        user = parsed.username or "postgres",
        password = parsed.password or "",
        host = parsed.hostname or "",
        port = parsed.port or 5432,
        database = parsed.path.lstrip('/') if parsed.path else "postgres"
        
        # host=os.getenv("SUPABASE_DB_HOST"),
        # database=os.getenv("SUPABASE_DB_NAME"),
        # user=os.getenv("SUPABASE_DB_USER"),
        # password=os.getenv("SUPABASE_DB_PASSWORD"),
        # port=os.getenv("SUPABASE_DB_PORT"),
    )
