"""Creates the demo account through the real API. Usage (one command per line):
    export NBN_API=https://nothingbutnet-0l0a.onrender.com
    export NBN_DEMO_PASSWORD=nothingbutnet101
    python scripts/seed_demo.py ~/demo
"""
import os, sys, time
from pathlib import Path
import requests
 
API = os.environ["NBN_API"]
PW = os.environ["NBN_DEMO_PASSWORD"]
 
def signup_or_login(email, name, username):
    r = requests.post(f"{API}/auth/signup", json={"email": email, "password": PW, "name": name, "username": username}, timeout=120)
    if r.status_code == 400:                      # already exists → log in
        r = requests.post(f"{API}/auth/login", json={"email": email, "password": PW}, timeout=120)
    r.raise_for_status()
    return {"Authorization": f"Bearer {r.json()['token']}"}
 
def upload_and_wait(headers, clip):
    with open(clip, "rb") as f:
        up = requests.post(f"{API}/sessions/upload", headers=headers, files={"file": (clip.name, f, "video/mp4")}, timeout=300).json()
    requests.post(f"{API}/analysis/analyze", headers=headers, json={"session_id": up["session_id"], "video_url": up["video_url"]}, timeout=60)
    for _ in range(100):
        s = requests.get(f"{API}/sessions/{up['session_id']}", headers=headers, timeout=60).json()
        if s["status"] in ("done", "failed"):
            return s
        time.sleep(5)
    raise TimeoutError(clip.name)
 
demo = signup_or_login("demo@nothingbutnet.app", "Demo Player", "demo")
for clip in sorted(Path(sys.argv[1]).expanduser().glob("*.mp4")):
    s = upload_and_wait(demo, clip)
    made = "made" in clip.name.lower()
    requests.patch(f"{API}/sessions/{s['session_id']}", headers=demo, json={"made": made}, timeout=60)
    print(clip.name, s["status"], s.get("score"))
# then: two friends (signup_or_login), friend requests from demo, accept as each friend,
# and a few marked shots for each friend so the leaderboard has rows.
