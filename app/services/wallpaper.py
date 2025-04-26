import uuid
import time
import httpx

from ..helpers.upload import download_and_upload
from ..utils.web_id import WebId
from ..utils.ms_token import MsToken
from ..utils.tt_wid import TtWid
from ..utils.verify_fp import VerifyFp
from ..utils.headers import init_headers
from ..helpers.url_builder import build_douyin_wallpaper_url
from ..helpers.psycopg2 import get_connection

conn = get_connection()

def parse_and_insert_wallpaper_data(data: dict, conn):
    cursor = conn.cursor()
    wallpaper_list = data.get("wallpaper_list", [])
    if not wallpaper_list:
        return []

    formatted_results = []

    for item in wallpaper_list:
        try:
            aweme = item.get("aweme", {})
            if not aweme:
                continue

            # AUTHOR
            author = aweme.get("author", {})
            uid = author.get("uid")
            nickname = author.get("nickname")
            sec_uid = author.get("sec_uid")
            avatar_urls = author.get("avatar_thumb", {}).get("url_list", [])
            avatar = avatar_urls if avatar_urls else None
            signature = author.get("signature", "")
            username = author.get("unique_id") or f"user_{uid}"
            email = f"{username}@gmail.com"
            password = "placeholder_password"
            role = "user"

            cursor.execute('SELECT id FROM "Author" WHERE username = %s', (username,))
            author_row = cursor.fetchone()
            if not author_row:
                author_id = str(uuid.uuid4())
                cursor.execute(
                    """
                    INSERT INTO "Author" (id, username, email, password, "profilePic", bio, role, "createdAt", "updatedAt")
                    VALUES (%s, %s, %s, %s, %s, %s, %s, now(), now())
                    """,
                    (author_id, username, email, password, avatar, signature, role)
                )
            else:
                author_id = author_row[0]

            # MUSIC
            music = aweme.get("music", {})
            music_id = music.get("id_str")
            music_url = music.get("play_url", {}).get("uri", "")
            music_thumb = music.get("cover_thumb", {}).get("url_list", [None])
            if music_id:
                cursor.execute('SELECT id FROM "Music" WHERE id = %s', (music_id,))
                if not cursor.fetchone():
                    cursor.execute(
                        """
                        INSERT INTO "Music" (id, title, artist, url, duration, thumbnail, "createdAt")
                        VALUES (%s, %s, %s, %s, %s, %s, now())
                        """,
                        (
                            music_id,
                            music.get("title", ""),
                            music.get("author", ""),
                            music_url,
                            music.get("duration", 0),
                            music_thumb
                        )
                    )

            # VIDEO
            video = aweme.get("video", {})
            video_urls = video.get("play_addr", {}).get("url_list", [])
            video_url = video_urls if video_urls else [None]
            video_id = str(uuid.uuid4())
            cursor.execute(
                """
                INSERT INTO "Video" (id, "videoUrl", description, duration, "createdAt", "updatedAt", "authorId", title, "musicId", "thumbnailUrl")
                VALUES (%s, %s, %s, %s, to_timestamp(%s), now(), %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """,
                (
                    video_id,
                    video_url,
                    aweme.get("desc", ""),
                    video.get("duration", 0) // 1000,
                    aweme.get("create_time", 0),
                    author_id,
                    aweme.get("desc", "")[:20],
                    music_id,
                    video.get("cover", {}).get("url_list", [None])[0]
                )
            )

            # HASHTAGS
            for tag in aweme.get("text_extra", []):
                name = tag.get("hashtag_name")
                if name:
                    cursor.execute('SELECT id FROM "Hashtag" WHERE name = %s', (name,))
                    hashtag_row = cursor.fetchone()
                    if not hashtag_row:
                        hashtag_id = str(uuid.uuid4())
                        cursor.execute('INSERT INTO "Hashtag" (id, name) VALUES (%s, %s)', (hashtag_id, name))
                    else:
                        hashtag_id = hashtag_row[0]

                    cursor.execute(
                        """
                        INSERT INTO "VideoHashtag" (id, "videoId", "hashtagId")
                        VALUES (%s, %s, %s)
                        ON CONFLICT DO NOTHING
                        """,
                        (str(uuid.uuid4()), video_id, hashtag_id)
                    )

            # Return formatted result
            formatted_results.append({
                "author": {
                    "uid": uid,
                    "nickname": nickname,
                    "sec_uid": sec_uid,
                    "avatar": avatar_urls,
                    "signature": signature
                },
                "video": {
                    "aweme_id": aweme.get("aweme_id"),
                    "description": aweme.get("desc"),
                    "created_at": aweme.get("create_time"),
                    "duration": video.get("duration", 0) // 1000,
                    "video_url": video_url,
                    "thumbnail": video.get("cover", {}).get("url_list", [None])[0],
                    "video_id": video_id  # 👈 dùng để cập nhật chính xác
                },
                "music": {
                    "id_str": music_id,
                    "title": music.get("title"),
                    "author": music.get("author"),
                    "url": music_url,
                    "duration": music.get("duration"),
                    "thumbnail": music_thumb
                }
            })

        except Exception as e:
            print(f"[!] Skipping one item due to error: {e}")

    conn.commit()
    cursor.close()
    return formatted_results

async def upload_and_update_video(video_info: dict):
    try:
        video_urls = video_info["video"]["video_url"]
        video_id = video_info["video"]["video_id"]

        if not video_urls:
            return

        raw_url = video_urls[0]
        public_url = await download_and_upload(raw_url)

        with conn.cursor() as cursor:
            cursor.execute(
                'UPDATE "Video" SET "videoUrl" = %s WHERE id = %s',
                (public_url, video_id)
            )
            conn.commit()
    except Exception as e:
        conn.rollback()


async def crawl_wallpaper_videos(cursor: int = 6, UIFID_TEMP: str = None, UIFID: str = None, proxy: str = None) -> dict:
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
        results = parse_and_insert_wallpaper_data(data, conn)

    return results
