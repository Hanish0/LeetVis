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

class SupabaseClient:
    """Wrapper class for Supabase operations"""
    
    def __init__(self):
        self._client = None
    
    def get_client(self) -> Client:
        if self._client is None:
            try:
                self._client = create_client(SUPABASE_URL, SUPABASE_KEY)
            except Exception as e:
                print(f"Error creating Supabase client: {e}")
                raise
        return self._client

# Global instance
db_client = SupabaseClient()