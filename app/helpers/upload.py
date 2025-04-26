import uuid
import os
import tempfile
import httpx

from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def download_video(video_url: str) -> str:
    if not video_url.startswith("http://") and not video_url.startswith("https://"):
        raise ValueError(f"Invalid video URL: {video_url}")

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(video_url)
        response.raise_for_status()

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_file.write(response.content)
        temp_file.close()

        return temp_file.name 

def upload_to_supabase(file_path: str, file_name: str, bucket="tiktok") -> str:
    with open(file_path, "rb") as f:
        supabase.storage.from_(bucket).upload(file_name, f, {"content-type": "video/mp4"})
    
    public_url = supabase.storage.from_(bucket).get_public_url(file_name)
    return public_url

async def download_and_upload(video_url: str) -> str:
    temp_path = await download_video(video_url)
    try:
        max_size_mb = 49
        if os.path.getsize(temp_path) > max_size_mb * 1024 * 1024:
            raise Exception("File too large for Supabase upload")
        
        file_name = f"{uuid.uuid4()}.mp4"
        public_url = upload_to_supabase(temp_path, file_name)
        return public_url
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)