# notify_telegram.py
import requests, os
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def alert(msg):
    """Send Telegram message"""
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Telegram not configured:", msg)
        return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": msg}
        requests.get(url, params=params)
    except Exception as e:
        print("Telegram error:", e)
