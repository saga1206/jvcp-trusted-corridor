import os
from google import genai
from django.contrib.auth.models import User

client = genai.Client(api_key=os.environ.get("LLM_API_KEY"))

ASSISTANT_SYSTEM_PROMPT = """You are a multilingual assistant (Vietnamese, Japanese, English) for a platform
helping Vietnamese people in Japan with: travel, transportation, accommodation, local services,
payments, refunds, marketplace, and trusted providers.

Answer only platform/logistics questions. Do NOT give legal, immigration, financial, or medical advice —
if asked, say you can't advise on that and suggest contacting an official source or professional.
Reply in the same language the user writes in, unless they ask you to switch.
Keep answers concise and practical."""

def get_reply(user, history, new_message):
    context_note = f"User's preferred language on file: {getattr(user.identity_profile, 'preferred_language', 'vi') if hasattr(user, 'identity_profile') else 'vi'}."

    contents = []
    for m in history:
        contents.append({"role": "user" if m.role == "user" else "model", "parts": [{"text": m.content}]})
    contents.append({"role": "user", "parts": [{"text": new_message}]})

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config={"system_instruction": ASSISTANT_SYSTEM_PROMPT + "\n" + context_note},
    )
    return response.text.strip()