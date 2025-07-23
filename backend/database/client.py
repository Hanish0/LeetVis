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
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Use service key if available (for admin operations), otherwise use anon key
ACTIVE_KEY = SUPABASE_SERVICE_KEY if SUPABASE_SERVICE_KEY else SUPABASE_KEY

if not SUPABASE_URL or not ACTIVE_KEY:
    raise ValueError("SUPABASE_URL and either SUPABASE_ANON_KEY or SUPABASE_SERVICE_KEY environment variables are required")

print(f"Using {'service' if SUPABASE_SERVICE_KEY else 'anonymous'} key for Supabase")

# Database table names
VIDEOS_TABLE = "videos"
PROBLEMS_TABLE = "problems"

# Create Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, ACTIVE_KEY)
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