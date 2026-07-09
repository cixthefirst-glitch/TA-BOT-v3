import requests

from config import (
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
    TELEGRAM_URL
)


def send_message(text, chat_id=None):

    if chat_id is None:
        chat_id = TELEGRAM_CHAT_ID

    url = TELEGRAM_URL.format(
        token=TELEGRAM_TOKEN,
        method="sendMessage"
    )

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        requests.post(
            url,
            json=payload,
            timeout=15
        )

    except Exception as e:
        print("Telegram Error:", e)


def format_signal(signal):

    emoji = "🟢" if signal["side"] == "LONG" else "🔴"

    text = f"""
{emoji} <b>{signal['side']} {signal['symbol']}</b>

🎯 Confidence: {signal['confidence']:.1f}%

💰 Entry: {signal['entry']:.6f}

🛑 Stop: {signal['stop']:.6f}

🎯 TP1: {signal['tp1']:.6f}
🎯 TP2: {signal['tp2']:.6f}
🎯 TP3: {signal['tp3']:.6f}

⚖️ RR: {signal['rr']:.2f}

🧠 SMC:
{signal['smc']}

Reasons:
"""

    for reason in signal["reasons"]:
        text += f"\n✅ {reason}"

    return text