import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Dict, Any, Optional
from datetime import datetime

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables are required")

# Database table names
VIDEOS_TABLE = "videos"
PROBLEMS_TABLE = "problems"

# Create Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Failed to create Supabase client: {e}")
    raise

class SupabaseClient:
    """Wrapper class for Supabase operations"""
    
    def __init__(self):
        self.client = supabase
    
    def get_client(self) -> Client:
        return self.client

# Global instance
db_client = SupabaseClient()