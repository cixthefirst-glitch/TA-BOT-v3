import requests

from config import GEMINI_API_KEY, GEMINI_URL


def ask_gemini(signal):

    if not GEMINI_API_KEY:
        return True, "Gemini Disabled"

    prompt = f"""
You are a professional crypto analyst.

Evaluate this futures trade.

Symbol:
{signal['symbol']}

Side:
{signal['side']}

Confidence:
{signal['confidence']}

Risk Reward:
{signal['rr']:.2f}

Reasons:

{", ".join(signal["reasons"])}

Reply with ONLY YES or NO.
"""

    try:

        response = requests.post(

            f"{GEMINI_URL}?key={GEMINI_API_KEY}",

            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            },

            timeout=20

        )

        data = response.json()

        reply = data["candidates"][0]["content"]["parts"][0]["text"]

        reply = reply.upper()

        return "YES" in reply, reply

    except Exception as e:

        print(e)

        return True, "Gemini Error"