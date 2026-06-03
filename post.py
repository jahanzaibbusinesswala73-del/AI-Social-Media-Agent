import os
import requests
from datetime import datetime

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
FB_PAGE_ID = os.environ.get("FB_PAGE_ID")

topics = [
    "Karachi power outage and K-Electric failure",
    "Pakistan education system crisis",
    "Karachi roads and infrastructure corruption",
    "Political accountability in Pakistan",
    "Water crisis in Karachi",
]

def get_topic():
    day = datetime.now().day
    hour = datetime.now().hour
    index = (day + hour) % len(topics)
    return topics[index]

def generate_post(topic):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"""You are 'Karachi Voice' - a bold civic awareness page.
Write a short impactful Facebook post about: {topic}
- Max 100 words
- English only
- End with #KarachiVoice #Pakistan #Karachi
Just write the post, nothing else."""
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=data)
    result = response.json()
    print("Gemini response:", result)
    if "candidates" in result:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Karachi needs change! {topic} is a serious issue affecting millions. Time for accountability! #KarachiVoice #Pakistan #Karachi"

def post_to_facebook(message):
    url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
    data = {"message": message, "access_token": FB_ACCESS_TOKEN}
    response = requests.post(url, data=data)
    print("Facebook response:", response.json())
    return response.json()

topic = get_topic()
print(f"Topic: {topic}")
post_text = generate_post(topic)
print(f"Generated post:\n{post_text}")
result = post_to_facebook(post_text)
print(f"Posted: {result}")
