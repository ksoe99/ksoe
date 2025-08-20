# searchverify.py — Confirms if mirror URLs are indexed

import os, requests, json

MIRROR_LOG = "variant_log.csv"
INDEX_STATUS = "index_status.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; IndexCheckBot/1.0)"
}

def is_indexed(url):
    try:
        r = requests.get("https://www.google.com/search", params={"q": f"site:{url}"}, headers=HEADERS, timeout=10)
        return url in r.text
    except:
        return False

results = {}

if os.path.exists(MIRROR_LOG):
    with open(MIRROR_LOG, encoding="utf-8") as f:
        for line in f:
            if line.startswith("timestamp"): continue
            parts = line.strip().split(",")
            url_hash = parts[1]
            variant_id = parts[2]
            mirror_url = f"https://ksoe99.github.io/ksoe/{url_hash}_v{variant_id}/"
            status = is_indexed(mirror_url)
            results[mirror_url] = status

with open(INDEX_STATUS, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"[DONE] Index check complete. Results written to {INDEX_STATUS}")
