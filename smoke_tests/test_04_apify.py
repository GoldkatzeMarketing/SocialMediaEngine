"""
Smoke Test 4: Apify Instagram Scraper
- Scraped 1 Reel von EINEM Profil aus der Watchlist
- Validiert: API-Token, Actor laeuft, Cost-Estimate
- Kosten: ~$0.01
"""
import json
from pathlib import Path
from _helpers import require, ok, fail

PROJECT_ROOT = Path(__file__).parent.parent
CHANNELS_FILE = PROJECT_ROOT / "monitoring" / "instagram_channels.txt"


def main():
    token = require("APIFY_API_TOKEN")

    try:
        from apify_client import ApifyClient
    except ImportError:
        fail("apify-client not installed", ImportError("pip install -r requirements.txt"))

    if not CHANNELS_FILE.exists():
        fail(f"Channels file missing: {CHANNELS_FILE}")
        return

    channels = [
        line.strip()
        for line in CHANNELS_FILE.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if not channels:
        fail("Keine Profile in instagram_channels.txt")
        return

    target = channels[0]
    ok(f"Teste mit erstem Profil: {target}")

    client = ApifyClient(token)
    run_input = {
        "directUrls": [target],
        "resultsType": "posts",
        "resultsLimit": 1,
        "onlyPostsNewerThan": "1 week",
    }

    try:
        ok("Starte Apify-Actor 'apify/instagram-scraper' (kann 30-60s dauern)...")
        run = client.actor("apify/instagram-scraper").call(run_input=run_input, timeout_secs=120)
        ok(f"Actor-Run abgeschlossen: {run['id']}")

        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        if not items:
            print("⚠️  Keine Posts gefunden (Profil eventuell privat oder kein Content in letzter Woche).")
            return

        post = items[0]
        ok(f"Reel gefunden: {post.get('shortCode', '?')}")
        print(f"   Caption: {(post.get('caption') or '')[:80]}...")
        print(f"   Video-URL: {post.get('videoUrl', 'kein Video')}")
        print(f"   Likes: {post.get('likesCount', '?')}, Plays: {post.get('videoPlayCount', '?')}")

        stats = run.get("stats", {})
        cost = stats.get("computeUnits", 0) * 0.25
        print(f"\n💰 Geschaetzte Kosten dieses Tests: ~${cost:.4f}")

        out = Path(__file__).parent / "_apify_sample.json"
        out.write_text(json.dumps(post, indent=2, ensure_ascii=False, default=str))
        ok(f"Sample-Daten gespeichert: {out.name}")
    except Exception as e:
        fail("Apify-Scraper failed", e)


if __name__ == "__main__":
    main()
