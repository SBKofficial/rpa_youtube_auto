# generate_quote.py
import random
from config import OPENAI_API_KEY

FALLBACK_QUOTES = [
    "When silence speaks, listen closely.",
    "The smallest promise can hold the largest courage.",
    "Leave behind the version that doubts itself.",
    "We measure time by the steps we take, not the breaths we waste.",
    "Some journeys begin the moment you stop pretending."
]

def generate_with_openai():
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        prompt = (
            "Write 1 short cinematic dialogue line suitable for a 6-9 second Short. "
            "Also return a 6-10 word SEO title, a 1-line description and 6 hashtags. "
            "Return as plain text with sections separated by '||'."
        )

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )

        txt = resp.choices[0].message.content.strip()
        parts = txt.split("||")

        if len(parts) >= 4:
            quote = parts[0].strip()
            title = parts[1].strip()
            desc = parts[2].strip()
            tags = [t.strip() for t in parts[3].split(",")][:10]
            return {"quote": quote, "title": title, "description": desc, "tags": tags}

    except Exception as e:
        print("OpenAI error:", e)

    return None


def generate_quote():
    if OPENAI_API_KEY:
        result = generate_with_openai()
        if result:
            return result

    q = random.choice(FALLBACK_QUOTES)
    title = q if len(q) < 60 else q[:57] + "..."
    description = q + " — Cinematic Insight Lab"
    tags = ["moviequotes", "lifequotes", "shorts", "dialogue", "cinema", "quotes"]

    return {"quote": q, "title": title, "description": description, "tags": tags}
