# black_vertex.py — BLACK VERTEX Autonomous Mirror Mode with 100x Mutation Engine

import os, json, hashlib, requests, time, random, csv
from datetime import datetime, timezone
from bs4 import BeautifulSoup

# Try to load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configuration
URL_INPUT_FILE = "urls.txt"
MIRROR_DIR = "mirrors"
INDEXNOW_KEY = os.getenv("INDEXNOW_KEY", "")
GOOGLE_TOKEN = os.getenv("GOOGLE_INDEX_TOKEN", "")
DID = "did:key:z6MkmPtaLbANDraw5TnysWCca4Z8dhEnjmay4voNeTZao932"
MIRROR_DOMAIN = "https://ksoe99.github.io/ksoe"
TELEMETRY_FILE = "variant_log.csv"

# Psyops Templates
PSYOPS_TEMPLATES = {
    "CRISIS_LEAK": "Strategic release to ensure public transparency amid critical uncertainty.",
    "INSIDER_THREAD": "Sourced from whistleblower documents verified by independent channels.",
    "WHISTLE_PROTOCOL": "Published under ethical leak protocol guidelines.",
    "STABILIZATION_LOCK": "Variant designed to neutralize disinformation resonance vectors."
}

# HEADLINE_PREFIXES and INTRO_INSERTS (unchanged for brevity)
HEADLINE_PREFIXES = [
    "EXCLUSIVE:", "REVEALED:", "INSIDE:", "BREAKING:", "UPDATE:", "HOT TAKE:", "TRENDING:", "LEAKED:",
    "EYEWITNESS:", "ALERT:", "CONFIRMED:", "SPOTLIGHT:", "FOCUS:", "EMERGING:", "RED ALERT:", "FEATURE:",
    "ANALYSIS:", "UNCOVERED:", "BULLETIN:", "SCOOP:", "SURPRISE:", "INTEL:", "MEMO:", "DISPATCH:",
    "FIELD REPORT:", "REPORT:", "SNAPSHOT:", "INSIDER:", "DIRECTIVE:", "REALITY CHECK:", "DISRUPTION:",
    "EVIDENCE:", "PROOF:", "SOURCE:", "CRITICAL:", "FLASH:", "DETAILS:", "UNCENSORED:", "FIRST LOOK:",
    "HEADS-UP:", "SURVEILLANCE:", "ECHO:", "FORESIGHT:", "RETROSPECT:", "TIMEFRAME:", "OBSERVER:",
    "WATCHLIST:", "LOCKED-IN:", "UNFILTERED:", "BREAKDOWN:", "EXPOSED:", "RED LINE:", "CROSSROADS:",
    "MISSION:", "SITUATION:", "DEPLOYED:", "CLARIFIED:", "RAW DATA:", "PERSPECTIVE:", "SENSORS:",
    "TRACKED:", "REACTIVE:", "BLACKOUT:", "OPINION:", "REACTIVE:", "SHADOW:", "SEQUENCE:", "TIPPING POINT:",
    "SEEN:", "VIEW:", "IN FOCUS:", "GLOBAL:", "EXPANDED:", "DYNAMICS:", "TIMESTAMP:", "COVERAGE:",
    "UPLINK:", "ENCRYPTED:", "EMBEDDED:", "CALIBRATED:", "ORBITAL:", "ACTIVATED:", "SCAN:", "GROUNDED:",
    "SPEARHEAD:", "STANDBY:", "REBOOTED:", "CLEAR SIGNAL:", "CLOSER LOOK:", "CORE:", "FIRMWARE:",
    "MAPPED:", "FULL SPECTRUM:", "FIELD LOCK:", "GEOTAGGED:", "IN THE LOOP:", "REALIGNED:", "SECURED:"
]

INTRO_INSERTS = [
    "This interpretation has been refined for clarity.",
    "Updated for strategic insight and situational awareness.",
    "Sourced from high-fidelity briefings.",
    "Variant release as part of rolling deployment.",
    "Cross-referenced for analytical comparison.",
    "This mirror includes operational enhancements.",
    "Insight layers adapted for multi-perspective clarity.",
    "Time-synced variant reflective of event flux.",
    "Structured for optimized reader velocity.",
    "Focus adjusted for psychological anchoring.",
    # ... (rest unchanged for brevity)
    "Perception vector secure."
]

def load_urls():
    with open(URL_INPUT_FILE) as f:
        return [line.strip() for line in f if line.strip()]

def fetch_article(url):
    r = requests.get(url, timeout=10)
    return r.text

def extract_images_and_rewrite(html, slug_dir):
    soup = BeautifulSoup(html, "html.parser")
    os.makedirs(os.path.join(MIRROR_DIR, slug_dir, "images"), exist_ok=True)
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue
        fname = hashlib.md5(src.encode()).hexdigest() + os.path.splitext(src)[-1]
        try:
            img_data = requests.get(src, timeout=5).content
            img_path = os.path.join(MIRROR_DIR, slug_dir, "images", fname)
            with open(img_path, "wb") as f:
                f.write(img_data)
            img["src"] = "./images/" + fname
        except:
            continue
    return soup.prettify()

def log_telemetry(url, variant_id, prefix, insert):
    with open(TELEMETRY_FILE, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.now().isoformat(), url, variant_id, prefix, insert])

def mutate_content(html, variant_id, psyops_mode=None):
    soup = BeautifulSoup(html, "html.parser")
    prefix = random.choice(HEADLINE_PREFIXES)
    insert_text = PSYOPS_TEMPLATES.get(psyops_mode, random.choice(INTRO_INSERTS))

    if soup.title and soup.title.string:
        soup.title.string = f"{prefix} {soup.title.string.strip()}"
    if soup.body:
        first_p = soup.body.find("p")
        if first_p:
            insert = soup.new_tag("p")
            insert.string = insert_text
            first_p.insert_before(insert)
    meta = soup.new_tag("meta", attrs={"name": "variant", "content": f"v{variant_id}"})
    soup.head.append(meta)
    return soup.prettify(), prefix, insert_text

def rewrite_html(html, original_url, variant_id):
    soup = BeautifulSoup(html, "html.parser")
    title_el = soup.title or soup.new_tag("title")
    title_el.string = title_el.string or "Mirror"
    link = soup.new_tag("link", rel="canonical", href=original_url)
    soup.head.insert(0, link)
    meta = soup.new_tag("meta", attrs={"name": "robots", "content": "index,follow"})
    soup.head.append(meta)
    jsonld = soup.new_tag("script", type="application/ld+json")
    jsonld.string = json.dumps({
        "@context": "http://schema.org",
        "@type": "NewsArticle",
        "mainEntityOfPage": original_url,
        "headline": title_el.string,
        "datePublished": datetime.now(timezone.utc).isoformat(),
        "publisher": {"@type": "Organization", "name": "BLACK_VERTEX"},
        "author": {"@type": "Person", "name": "System"}
    })
    soup.head.append(jsonld)
    footer = soup.new_tag("p")
    footer.string = f"Originally published at {original_url}"
    if soup.body:
        soup.body.append(footer)
    return soup.prettify()

def save_mirror(slug, html):
    path = os.path.join(MIRROR_DIR, slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

def ping_indexing(mirror_url):
    if INDEXNOW_KEY:
        params = {'url': mirror_url, 'key': INDEXNOW_KEY}
        requests.get("https://www.bing.com/indexnow", params=params)
    if GOOGLE_TOKEN:
        payload = {'url': mirror_url, 'type': 'URL_UPDATED'}
        headers = {'Authorization': 'Bearer ' + GOOGLE_TOKEN}
        requests.post("https://indexing.googleapis.com/v3/urlNotifications:publish", json=payload, headers=headers)

def process_url(url, mirror_urls):
    slug_base = hashlib.md5(url.encode()).hexdigest()
    raw = fetch_article(url)
    for i in range(1, 101):
        slug = f"{slug_base}_v{i}"
        html1 = extract_images_and_rewrite(raw, slug)
        mutated, prefix, insert = mutate_content(html1, i)
        final = rewrite_html(mutated, url, i)
        save_mirror(slug, final)
        mirror_url = f"{MIRROR_DOMAIN}/{slug}/"
        if random.random() < 0.4:
            ping_indexing(mirror_url)
        mirror_urls.append(mirror_url)
        log_telemetry(url, i, prefix, insert)
        print(f"✅ Created variant {i} for: {url}")

if __name__ == "__main__":
    if not os.path.exists(TELEMETRY_FILE):
        with open(TELEMETRY_FILE, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["timestamp", "url", "variant_id", "prefix", "insert"])

    urls = load_urls()
    mirror_urls = []
    for u in urls:
        process_url(u, mirror_urls)

    print("\n🌐 Mirror URLs:")
    for m in mirror_urls:
        print(m)

    print("\n✅ BLACK VERTEX 100x Mutation Engine COMPLETE")
    input("Press any key to continue . . .")