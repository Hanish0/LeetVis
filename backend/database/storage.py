"""
Supabase Storage service for handling video file uploads and downloads.
This replaces the base64 video storage in the database with proper file storage.
"""

import os
from typing import Optional, Dict, Any
from supabase import Client
try:
    from .client import db_client
except ImportError:
    from client import db_client
import uuid
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

class SupabaseStorageService:
    """Service for managing video files in Supabase Storage using S3 SDK"""
    
    BUCKET_NAME = "videos"  # Supabase storage bucket name
    
    def __init__(self):
        self.client: Client = db_client.get_client()
        self.s3_client = self._create_s3_client()
        self._ensure_bucket_exists()
    
    def _create_s3_client(self):
        """Create S3 client for Supabase Storage"""
        try:
            # Get S3 credentials from environment
            access_key_id = os.getenv("SUPABASE_S3_ACCESS_KEY_ID")
            secret_access_key = os.getenv("SUPABASE_S3_SECRET_ACCESS_KEY")
            endpoint_url = os.getenv("SUPABASE_S3_ENDPOINT")
            region = os.getenv("SUPABASE_S3_REGION", "us-east-1")
            
            # Fallback to auto-detection if specific S3 vars not set
            if not all([access_key_id, secret_access_key, endpoint_url]):
                print("🔄 S3 credentials not found, auto-detecting from Supabase settings...")
                
                supabase_url = os.getenv("SUPABASE_URL")
                if not supabase_url:
                    raise ValueError("SUPABASE_URL not found")
                
                # Extract project ref from URL
                project_ref = supabase_url.split("//")[1].split(".")[0]
                access_key_id = project_ref
                secret_access_key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")
                endpoint_url = f"https://{project_ref}.supabase.co/storage/v1/s3"
            
            if not secret_access_key:
                raise ValueError("No service key found for S3 authentication")
            
            print(f"🔗 S3 Endpoint: {endpoint_url}")
            print(f"🔑 Access Key: {access_key_id}")
            print(f"🌍 Region: {region}")
            
            s3_client = boto3.client(
                's3',
                endpoint_url=endpoint_url,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region,
                config=boto3.session.Config(
                    s3={'addressing_style': 'path'}  # Force path style for Supabase
                )
            )
            
            print(f"✅ S3 client created for Supabase Storage")
            return s3_client
            
        except Exception as e:
            print(f"❌ Failed to create S3 client: {e}")
            print("   Falling back to Supabase client")
            return None
    
    def _ensure_bucket_exists(self):
        """Ensure the videos bucket exists in Supabase Storage"""
        print(f"🔍 Checking storage bucket '{self.BUCKET_NAME}'...")
        
        # For S3-authenticated storage, we'll skip the bucket existence check
        # and let the upload operation handle bucket validation
        # This avoids authentication issues with bucket listing operations
        
        print(f"📝 Note: Using S3-authenticated storage")
        print(f"   Bucket operations will be validated during upload")
        print(f"   If bucket doesn't exist, upload will fail with clear error")
        
        # We'll validate bucket access during the first upload attempt
        # This is more reliable than trying to list/get bucket info with limited permissions
    
    def upload_video(self, video_path: str, problem_title: str, language: str, video_type: str) -> Optional[str]:
        """
        Upload video file to Supabase Storage using S3 SDK.
        
        Args:
            video_path: Local path to the video file
            problem_title: Title of the LeetCode problem
            language: Programming language (python, java, cpp)
            video_type: Type of video (explanation, brute_force, optimal)
            
        Returns:
            Public URL of the uploaded video or None if upload failed
        """
        try:
            # Generate unique filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            safe_title = problem_title.lower().replace(" ", "_").replace("-", "_")
            filename = f"{safe_title}_{language}_{video_type}_{timestamp}.mp4"
            
            print(f"📤 Uploading {filename} to Supabase Storage...")
            
            # Try S3 upload first if S3 client is available
            if self.s3_client:
                try:
                    # Upload using S3 SDK
                    with open(video_path, 'rb') as video_file:
                        self.s3_client.upload_fileobj(
                            video_file,
                            self.BUCKET_NAME,
                            filename,
                            ExtraArgs={
                                'ContentType': 'video/mp4',
                                'CacheControl': 'max-age=3600'
                            }
                        )
                    
                    # Generate public URL
                    supabase_url = os.getenv("SUPABASE_URL")
                    project_ref = supabase_url.split("//")[1].split(".")[0]
                    public_url = f"{supabase_url}/storage/v1/object/public/{self.BUCKET_NAME}/{filename}"
                    
                    print(f"✅ Video uploaded successfully via S3: {filename}")
                    print(f"🌐 Public URL: {public_url}")
                    return public_url
                    
                except ClientError as e:
                    print(f"❌ S3 upload failed: {e}")
                    print("   Falling back to Supabase client...")
                except Exception as e:
                    print(f"❌ S3 upload error: {e}")
                    print("   Falling back to Supabase client...")
            
            # Fallback to Supabase client
            with open(video_path, 'rb') as video_file:
                video_data = video_file.read()
            
            response = self.client.storage.from_(self.BUCKET_NAME).upload(
                filename,
                video_data,
                file_options={
                    "content-type": "video/mp4",
                    "cache-control": "3600",
                    "upsert": False
                }
            )
            
            if response and not response.get('error'):
                public_url = self.client.storage.from_(self.BUCKET_NAME).get_public_url(filename)
                print(f"✅ Video uploaded successfully via Supabase client: {filename}")
                return public_url
            else:
                error_msg = response.get('error', 'Unknown error') if response else 'No response'
                print(f"❌ Supabase client upload failed: {error_msg}")
                return None
            
        except Exception as e:
            print(f"❌ Error uploading video to storage: {e}")
            return None
    
    def get_video_url(self, problem_title: str, language: str, video_type: str) -> Optional[str]:
        """
        Get the public URL for a video from the database.
        
        Args:
            problem_title: Title of the LeetCode problem
            language: Programming language
            video_type: Type of video
            
        Returns:
            Public URL of the video or None if not found
        """
        try:
            try:
                from .service import DatabaseService
            except ImportError:
                from service import DatabaseService
            video_record = DatabaseService.get_video(problem_title, language, video_type)
            
            if video_record and video_record.get('storage_url'):
                return video_record['storage_url']
            
            return None
            
        except Exception as e:
            print(f"Error getting video URL: {e}")
            return None
    
    def delete_video(self, storage_url: str) -> bool:
        """
        Delete a video file from Supabase Storage using S3 SDK.
        
        Args:
            storage_url: The public URL of the video to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            # Extract filename from URL
            filename = storage_url.split('/')[-1]
            
            print(f"🗑️  Deleting {filename} from Supabase Storage...")
            
            # Try S3 delete first if S3 client is available
            if self.s3_client:
                try:
                    self.s3_client.delete_object(Bucket=self.BUCKET_NAME, Key=filename)
                    print(f"✅ Video deleted successfully via S3: {filename}")
                    return True
                except ClientError as e:
                    print(f"❌ S3 delete failed: {e}")
                    print("   Falling back to Supabase client...")
                except Exception as e:
                    print(f"❌ S3 delete error: {e}")
                    print("   Falling back to Supabase client...")
            
            # Fallback to Supabase client
            response = self.client.storage.from_(self.BUCKET_NAME).remove([filename])
            
            if response:
                print(f"✅ Video deleted successfully via Supabase client: {filename}")
                return True
            else:
                print(f"❌ Supabase client delete failed")
                return False
            
        except Exception as e:
            print(f"❌ Error deleting video from storage: {e}")
            return False
    
    def get_signed_url(self, filename: str, expires_in: int = 3600) -> Optional[str]:
        """
        Generate a signed URL for private video access.
        
        Args:
            filename: Name of the file in storage
            expires_in: URL expiration time in seconds (default: 1 hour)
            
        Returns:
            Signed URL that expires after specified time
        """
        try:
            response = self.client.storage.from_(self.BUCKET_NAME).create_signed_url(
                filename, 
                expires_in
            )
            
            if response and 'signedURL' in response:
                return response['signedURL']
            return None
            
        except Exception as e:
            print(f"Error creating signed URL: {e}")
            return None
    
    def list_videos(self) -> list:
        """
        List all videos in the storage bucket.
        
        Returns:
            List of video file information
        """
        try:
            response = self.client.storage.from_(self.BUCKET_NAME).list()
            return response if response else []
            
        except Exception as e:
            print(f"Error listing videos: {e}")
            return []

# Global storage service instance
storage_service = SupabaseStorageService()

if __name__ == "__main__":
    print("Supabase Storage Service initialized successfully!")
    print(f"Bucket name: {storage_service.BUCKET_NAME}")
    print("Storage service is ready to use.")