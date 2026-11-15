"""One-command check of the core flow. Usage:
   export NBN_API=https://nothingbutnet-0l0a.onrender.com
   python scripts/smoke_test.py ml/tests/data/pose_clip.mp4
"""
import os, sys, time, uuid
import requests

API = os.environ.get("NBN_API", "http://localhost:8000")

if len(sys.argv) < 2:
    sys.exit("Usage: python scripts/smoke_test.py path/to/clip.mp4")
clip = sys.argv[1]
if not os.path.exists(clip):
    sys.exit(f"Clip not found: {clip}")

results = []

def step(name, fn):
    start = time.time()
    try:
        out = fn()
        results.append((name, "PASS"))
        print(f"PASS {name} ({time.time() - start:.1f}s)")
        return out
    except Exception as e:
        results.append((name, "FAIL"))
        print(f"FAIL {name} - {type(e).__name__}: {e}")
        print(f"\n{sum(r[1] == 'PASS' for r in results)} passed, 1 failed")
        sys.exit(1)

def ok(resp):
    if not resp.ok:
        raise RuntimeError(f"{resp.status_code}: {resp.text}")
    return resp.json()

print(f"Testing {API}\n")

step("health", lambda: requests.get(f"{API}/health", timeout=120).raise_for_status())

uid = uuid.uuid4().hex[:8]
email = f"smoke-{uid}@test.local"

def signup():
    r = requests.post(
        f"{API}/auth/signup",
        json={"body": {"email": email, "password": "smoke-test-1", "name": "Smoke"},
              "username": f"smoke{uid}"},
        timeout=60)
    if r.status_code == 422:
        print("WARN: new signup shape rejected, retrying old flat shape (server may be outdated)")
        r = requests.post(
            f"{API}/auth/signup",
            json={"email": email, "password": "smoke-test-1", "name": "Smoke"},
            timeout=60)
    return ok(r)["token"]

tok = step("signup", signup)
H = {"Authorization": f"Bearer {tok}"}

def upload():
    with open(clip, "rb") as f:
        return ok(requests.post(
            f"{API}/sessions/upload", headers=H,
            files={"file": (os.path.basename(clip), f, "video/mp4")},
            timeout=300))
up = step("upload", upload)

step("analyze", lambda: requests.post(
    f"{API}/analysis/analyze", headers=H,
    json={"session_id": up["session_id"], "video_url": up["video_url"]},
    timeout=60).raise_for_status())

def wait_done():
    for _ in range(100):
        s = ok(requests.get(f"{API}/sessions/{up['session_id']}", headers=H, timeout=60))
        if s["status"] == "done":
            return s
        if s["status"] == "failed":
            raise RuntimeError(s.get("error"))
        time.sleep(5)
    raise TimeoutError("analysis took over ~8 minutes")
step("analysis done", wait_done)

step("get session", lambda: ok(requests.get(
    f"{API}/sessions/{up['session_id']}", headers=H, timeout=60)))
step("list sessions", lambda: requests.get(f"{API}/sessions", headers=H, timeout=60).raise_for_status())
step("progress", lambda: requests.get(f"{API}/progress", headers=H, timeout=60).raise_for_status())

print(f"\nAll {len(results)} steps passed")