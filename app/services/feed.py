import time
import httpx
from ..utils.web_id import WebId
from ..utils.ms_token import MsToken
from ..utils.tt_wid import TtWid
from ..utils.verify_fp import VerifyFp
from ..utils.headers import init_headers
from ..helpers.url_builder import build_douyin_feed_url

def format_douyin_response(data: dict) -> list[dict]:
    videos = data.get("aweme_list", [])
    formatted = []

    for v in videos:
        video_id = v.get("aweme_id")
        video = v.get("video") or {}
        video_url = (video.get("play_addr") or {}).get("url_list", [None])

        if not video_id or not video_url:
            continue

        desc = v.get("desc", "")
        caption = v.get("text_extra") or []
        author = v.get("author") or {}
        stats = v.get("statistics") or {}
        share = v.get("share_info") or {}
        avatar_url = (author.get("avatar_thumb") or {}).get("url_list", [None])

        formatted.append({
            "video_id": video_id,
            "description": desc,
            "caption_tags": [tag.get("hashtag_name", "") for tag in caption if isinstance(tag, dict)],
            "created_at": v.get("create_time"),
            "author": {
                "nickname": author.get("nickname"),
                "user_id": author.get("uid"),
                "sec_uid": author.get("sec_uid"),
                "avatar": avatar_url
            },
            "stats": {
                "likes": stats.get("digg_count"),
                "comments": stats.get("comment_count"),
                "shares": stats.get("share_count"),
                "favorites": stats.get("collect_count")
            },
            "video_url": video_url,
            "share_url": share.get("share_url"),
            "resolution": f"{video.get('width', 0)}x{video.get('height', 0)}"
        })

    return formatted

async def crawl_feed_videos(page: int = 1, UIFID_TEMP: str = None, UIFID: str = None, proxy: str = None) -> dict:
    headers = init_headers()
    
    web_id = await WebId.get_web_id(headers)
    ms_token = await MsToken.get_real_ms_token(headers)
    tt_wid = await TtWid.get_tt_wid(headers)
    ts = int(time.time() * 1000)
    verify_fp = VerifyFp.get_verify_fp(ts)

    cookie = (
        f"ttwid={tt_wid};"
        f"UIFID_TEMP={UIFID_TEMP};"
        "hevc_supported=true; dy_swidth=1536; dy_sheight=864;"
        f"s_v_web_id={web_id};"
        "FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D;"
        "bd_ticket_guard_client_web_domain=2;"
        f"UIFID={UIFID};"
        "stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A8%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22"
    )
    
    headers["Cookie"] = cookie
    
    url = build_douyin_feed_url(refresh_index=page, webid=web_id, verifyFp=verify_fp, fp=verify_fp, msToken=ms_token)
 
    async with httpx.AsyncClient(proxy=proxy, headers=headers, timeout=15) as client:
        response = await client.get(url) 
        data = response.json()
        results = format_douyin_response(data)
        
    return results