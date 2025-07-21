#!/usr/bin/env python3
"""
Simple test script to verify database connection works.
Run this before starting the main server.
"""

try:
    from database.client import db_client
    print("✅ Database client imported successfully")
    
    client = db_client.get_client()
    print("✅ Supabase client created successfully")
    
    # Test a simple query
    response = client.table("problems").select("*").limit(1).execute()
    print("✅ Database connection test successful")
    print(f"Response: {response}")
    
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("\nTroubleshooting steps:")
    print("1. Make sure you have installed the requirements: pip install -r requirements.txt")
    print("2. Check your .env file has the correct SUPABASE_URL and SUPABASE_ANON_KEY")
    print("3. Make sure you have created the tables in Supabase (run: python -m database.init)")