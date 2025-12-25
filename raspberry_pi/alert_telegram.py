import os
import time
import requests

TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

COOLDOWN_SEC = 300  # 5 minutes
_last_sent = {}

def _send(text: str) -> bool:
    if not TOKEN or not CHAT_ID:
        return False
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    r = requests.post(url, data=payload, timeout=10)
    return r.status_code == 200

def _can_send(key: str) -> bool:
    now = time.time()
    last = _last_sent.get(key, 0)
    if now - last >= COOLDOWN_SEC:
        _last_sent[key] = now
        return True
    return False

def check_and_alert(mq2: float, mq135: float, temp_c: float, hum_pct: float, ai_label: str = None):
    # Thresholds (edit if you want)
    mq2_th = 600
    mq135_th = 600

    if mq2 >= mq2_th and _can_send("mq2_high"):
        _send(
            "ALERT: MQ2 HIGH\n"
            f"mq2={mq2:.0f}\n"
            f"mq135={mq135:.0f}\n"
            f"temp_c={temp_c:.1f}\n"
            f"hum_pct={hum_pct:.1f}\n"
            + (f"ai={ai_label}\n" if ai_label else "")
        )

    if mq135 >= mq135_th and _can_send("mq135_high"):
        _send(
            "ALERT: MQ135 HIGH\n"
            f"mq2={mq2:.0f}\n"
            f"mq135={mq135:.0f}\n"
            f"temp_c={temp_c:.1f}\n"
            f"hum_pct={hum_pct:.1f}\n"
            + (f"ai={ai_label}\n" if ai_label else "")
        )

    # If AI says Bad, send alert (optional)
    if ai_label == "Bad" and _can_send("ai_bad"):
        _send(
            "ALERT: AI PREDICTS BAD AIR QUALITY\n"
            f"mq2={mq2:.0f}, mq135={mq135:.0f}, temp_c={temp_c:.1f}, hum_pct={hum_pct:.1f}\n"
        )
