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
    
    # Videos table with Supabase Storage URLs
    videos_sql = """
-- Create videos table (stores Supabase Storage URLs only)
CREATE TABLE IF NOT EXISTS videos (
    id SERIAL PRIMARY KEY,
    problem_title VARCHAR(255) NOT NULL,
    language VARCHAR(20) NOT NULL CHECK (language IN ('python', 'java', 'cpp')),
    video_type VARCHAR(20) NOT NULL CHECK (video_type IN ('explanation', 'brute_force', 'optimal')),
    storage_url TEXT NOT NULL,  -- Supabase Storage public URL
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Ensure unique combination of problem, language, and video type
    UNIQUE(problem_title, language, video_type)
);

-- Create indexes for faster video lookups
CREATE INDEX IF NOT EXISTS idx_videos_lookup ON videos(problem_title, language, video_type);
CREATE INDEX IF NOT EXISTS idx_videos_created_at ON videos(created_at);
CREATE INDEX IF NOT EXISTS idx_videos_storage_url ON videos(storage_url);
"""
    
    print(problems_sql)
    print(videos_sql)
    
    print("\n=== Key Improvements ===")
    print("✅ Videos stored exclusively in Supabase Storage")
    print("✅ Clean database schema with storage URLs only")
    print("✅ Efficient video streaming via CDN")
    print("✅ Proper constraints and indexes for performance")
    print("✅ Unique constraints prevent duplicate videos")
    print("✅ Automatic bucket creation and management")
    
    print("\n=== Benefits ===")
    print("• High-performance video streaming via Supabase CDN")
    print("• Cost-effective storage separate from database")
    print("• Global video distribution and caching")
    print("• Scalable storage without database limitations")
    print("• Clean, maintainable codebase")
    print("• Automatic video file management and cleanup")

if __name__ == "__main__":
    print_database_schema()