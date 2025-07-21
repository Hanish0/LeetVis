"""
Database initialization script for Supabase.
This script creates the necessary tables in Supabase if they don't exist.

Note: In Supabase, you typically create tables through the dashboard or SQL editor.
This script provides the SQL commands you need to run in Supabase.
"""

# SQL commands to create tables in Supabase
CREATE_VIDEOS_TABLE = """
CREATE TABLE IF NOT EXISTS videos (
    id SERIAL PRIMARY KEY,
    problem_title VARCHAR(255) NOT NULL,
    language VARCHAR(50) NOT NULL,
    video_type VARCHAR(50) NOT NULL,
    video_path VARCHAR(500) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""

CREATE_PROBLEMS_TABLE = """
CREATE TABLE IF NOT EXISTS problems (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL UNIQUE,
    title_slug VARCHAR(255) NOT NULL UNIQUE,
    content TEXT,
    difficulty VARCHAR(50)
);
"""

def print_sql_commands():
    """Print SQL commands to run in Supabase SQL editor"""
    print("=== Run these SQL commands in your Supabase SQL Editor ===\n")
    
    print("1. Create videos table:")
    print(CREATE_VIDEOS_TABLE)
    print("\n" + "="*50 + "\n")
    
    print("2. Create problems table:")
    print(CREATE_PROBLEMS_TABLE)
    print("\n" + "="*50 + "\n")
    
    print("After running these commands, your database will be ready!")

if __name__ == "__main__":
    print_sql_commands()