from fastapi import APIRouter, HTTPException, Query
from ..services.feed import crawl_feed_videos
from ..services.wallpaper import crawl_wallpaper_videos
from dotenv import load_dotenv

import os

load_dotenv()
router = APIRouter()

PROXY_HOST = os.getenv("PROXY_HOST")
PROXY_PORT = os.getenv("PROXY_PORT")
PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")

PROXY_URL = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"

@router.get("/videos/feed")
async def get_feed_videos(
    UIFID_TEMP: str,
    UIFID: str,
    page: int = Query(1, ge=1)
):
    try:
        videos = await crawl_feed_videos(proxy=PROXY_URL, UIFID_TEMP=UIFID_TEMP, UIFID=UIFID, page=page)

        return {
            "page": page,
            "total": len(videos),
            "videos": videos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/videos/wallpaper")
async def get_wallpaper_videos(
    UIFID_TEMP: str,
    UIFID: str,
    cursor: int = Query(6, ge=6)
):
    try:
        videos = await crawl_wallpaper_videos(proxy=PROXY_URL, UIFID_TEMP=UIFID_TEMP, UIFID=UIFID, cursor=cursor)

        return {
            "cursor": cursor,
            "total": len(videos),
            "videos": videos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))