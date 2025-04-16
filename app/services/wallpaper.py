import time
import httpx
from ..utils.web_id import WebId
from ..utils.ms_token import MsToken
from ..utils.tt_wid import TtWid
from ..utils.verify_fp import VerifyFp
from ..utils.headers import init_headers
from ..url_builder import build_douyin_wallpaper_url


async def crawl_wallpaper_videos(cursor:int=6, UIFID_TEMP: str = None, UIFID: str = None, proxy: str = None) -> dict:
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
    
    url = build_douyin_wallpaper_url(cursor=cursor, webid=web_id, msToken=ms_token, uifid=UIFID, verify_fp=verify_fp)
 
    async with httpx.AsyncClient(proxy=proxy, headers=headers, timeout=15) as client:
        response = await client.get(url) 
        data = response.json()
        data
        
    return data