# autopush.py — Commit + Push all mirror changes to GitHub

import os, subprocess
from datetime import datetime

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
BRANCH = "main"  # or "gh-pages" if that's your GitHub Pages branch

os.chdir(REPO_DIR)

def git(cmd):
    result = subprocess.run(["git"] + cmd, capture_output=True, text=True)
    return result.stdout.strip()

changed = git(["status", "--porcelain"])
if not changed:
    print("[SKIP] No changes to commit.")
else:
    git(["add", "mirrors"])
    git(["add", "variant_log.csv"])
    commit_msg = f"Auto mirror push: {datetime.now().isoformat()}"
    git(["commit", "-m", commit_msg])
    git(["push", "origin", BRANCH])
    print("[OK] Mirrors pushed to GitHub.")
