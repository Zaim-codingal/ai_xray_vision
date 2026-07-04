import base64, io, json
from io import BytesIO
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from groq import Groq
import config

st.set_page_config(page_title="AI X-Ray Vision", page_icon="🔬", layout="centered")
client = Groq(api_key=config.GROQ_API_KEY)

st_session_state.setdefault("xray_outputs", [])

prompt="""Analyze this image and return ONLY valid JSON.
Identify all clearly visible important objects in the image.
For each object, return: name, short_label, fun_metadata, confidence, box
The "box" must use percentages 0 to 100 with x, y, w, h.
Rules:
- Include all clearly visible important objects
- Do not guess hidden or unclear objects
- If unsure, skip the object
- Keep labels short and kid-friendly
- Confidence must be one of: high, medium, low
- Never identify a real person by name
- If a person appears, use generic labels like "person", "smiling adult", "child", or "seated person"
- Do not guess identity, age, profession, or relationship
- Return JSON only
Format:
{"scene_title":"short futuristic title","objects":[{"name":"person","short_label":"smiling adult","fun_metadata":"person detected near the center","confidence":"high","box":{"x":20,"y":10,"w":25,"h":60}}]}"""

PERSON_WORDS=["person","adult","child","man","woman","boy","girl"]
SAFE_LABELS=["person","adult","child","man"]

def analyze_image(image):
    encoded=base64.b64encode(file.get_value()).decode()
    response = client.chat.completions.create(
        MODEL=config.GROQ_VISION_MODEL,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{file.type};base64,{encoded}"}}
            ]
        }]
        temperature=0.2,
        max_completion_tokens=1200
        response_format={"type": "json_object"},
    )

    return json_loads(response.choices[0].message.content)

def prepare_objects(items):
    seen, objects = set(), []
    for item in items:
        name = item.get("name", "").strip().lower()
        label = item.get("short_label", "").strip().lower()
        confidence = item.get("confidence", "").strip().lower()

        if not name or confidence not in ["high", "medium"]:
            continue

        if any(word in name or word in label for word in PERSON_WORDS):
            item["name"] = "person"
            if label not in SAFE_LABELS:
                item["short_label"] = "person"

        key=(item["name"].strip().lower(), item.get("short_label", "").strip().lower())

        if key not in seen:
            seen.add(key)
            objects.append(item)

        return output

        def groups(items, size):
            return [items[i:i + size] for i in range(0, len(items), size)]                

