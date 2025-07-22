"""
Database initialization script for LeetCode Video Generator.
Run this to see the SQL commands needed to set up your Supabase database.
"""

def print_database_schema():
    """Print the SQL commands needed to create the database tables"""
    
    print("=== LeetCode Video Generator Database Schema ===")
    print("\nRun these SQL commands in your Supabase SQL Editor:\n")
    
    # Problems table
    problems_sql = """
-- Create problems table
CREATE TABLE IF NOT EXISTS problems (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    title_slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT,
    difficulty VARCHAR(20) CHECK (difficulty IN ('Easy', 'Medium', 'Hard')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_problems_title ON problems(title);
CREATE INDEX IF NOT EXISTS idx_problems_title_slug ON problems(title_slug);
"""
    
    # Videos table with binary data storage
    videos_sql = """
-- Create videos table (stores actual video data, not file paths)
CREATE TABLE IF NOT EXISTS videos (
    id SERIAL PRIMARY KEY,
    problem_title VARCHAR(255) NOT NULL,
    language VARCHAR(20) NOT NULL CHECK (language IN ('python', 'java', 'cpp')),
    video_type VARCHAR(20) NOT NULL CHECK (video_type IN ('explanation', 'brute_force', 'optimal')),
    video_data TEXT NOT NULL,  -- Base64 encoded video data
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Ensure unique combination of problem, language, and video type
    UNIQUE(problem_title, language, video_type)
);

-- Create indexes for faster video lookups
CREATE INDEX IF NOT EXISTS idx_videos_lookup ON videos(problem_title, language, video_type);
CREATE INDEX IF NOT EXISTS idx_videos_created_at ON videos(created_at);
"""
    
    print(problems_sql)
    print(videos_sql)
    
    print("\n=== Key Improvements ===")
    print("✅ Videos stored as binary data (base64) in database")
    print("✅ No file path dependencies - works across all deployments")
    print("✅ Proper constraints and indexes for performance")
    print("✅ Unique constraints prevent duplicate videos")
    print("✅ Videos served directly from database")
    
    print("\n=== Benefits ===")
    print("• Videos accessible from any deployment environment")
    print("• No broken file path issues")
    print("• Centralized video storage")
    print("• Better security and access control")
    print("• Scalable across multiple server instances")

if __name__ == "__main__":
    print_database_schema()