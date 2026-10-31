#!/usr/bin/env python3
"""Download the newest release APK (prereleases included) for each repo in apps.txt."""
import json, os, re, sys, urllib.request
OWNER = os.environ.get("OWNER", "Victorious93")
TOKEN = os.environ.get("GH_TOKEN", "")
def api(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {})})
    return json.load(urllib.request.urlopen(req))
def pick(apks):
    names = [a["name"].lower() for a in apks]
    for pref in (lambda n: "universal" in n,
                 lambda n: not re.search(r"arm64|armeabi|x86|v7a|v8a", n),
                 lambda n: "arm64" in n):
        for a, n in zip(apks, names):
            if pref(n): return a
    return None
os.makedirs("repo", exist_ok=True)
skipped = []
for repo in [l.strip() for l in open("apps.txt") if l.strip() and not l.startswith("#")]:
    try:
        rels = api(f"https://api.github.com/repos/{OWNER}/{repo}/releases?per_page=20")
    except Exception as e:
        skipped.append((repo, f"api error {e}")); continue
    rels = [r for r in rels if not r.get("draft")]
    asset = None
    for r in rels:  # newest first
        apks = [a for a in r["assets"] if a["name"].endswith(".apk")]
        if apks:
            asset = pick(apks); tag = r["tag_name"]; break
    if not asset:
        skipped.append((repo, "no .apk asset")); continue
    dest = f"repo/{repo}-{re.sub(r'[^A-Za-z0-9._-]','_',tag)}.apk"
    print(f"{repo}: {tag} {asset['name']} -> {dest}")
    urllib.request.urlretrieve(asset["browser_download_url"], dest)
for r, why in skipped: print(f"SKIP {r}: {why}")
