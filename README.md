# Douyin API Crawler (FastAPI)

A high-performance crawler service built with **FastAPI** to extract video and wallpaper content from **Douyin (抖音)** without using the official API.  
This project **reverse-engineers** Douyin's internal endpoints and **fully replicates browser behavior** to generate all necessary tokens, without launching a browser.

---

## 🚀 Features

- 🔍 **Feed crawler**: Get videos from homepage feed.
- 🖼️ **Wallpaper crawler**: Fetch creative video wallpapers from `/web/wallpaper/item/`.
- 🧠 **No browser required**: `msToken`, `ttwid`, `verifyFp`, and even `a_bogus` are fully self-generated — no headless browser, no Selenium, no Playwright.
- 🛠️ **Fingerprint & session emulation**: Mimics real browser/device environment including screen, CPU, memory.
- 🌐 **Proxy support**: Crawl via optional rotating proxies.
- 📦 **Clean JSON API**: Powered by FastAPI with structured responses.

---

## 🧱 Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **HTTP Client**: [`httpx`](https://www.python-httpx.org/)
- **Token Emulation**:
  - ✅ `ttwid` generator
  - ✅ `s_v_web_id` / `verifyFp` with timestamp spoofing
  - ✅ `msToken` generation
  - ✅ `a_bogus` reverse-engineered implementation (ABogus)
