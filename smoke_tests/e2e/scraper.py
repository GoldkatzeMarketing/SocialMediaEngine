"""Apify Instagram-Scraper – holt das neueste Reel eines Profils."""
import os
import urllib.request
from pathlib import Path


def get_latest_reel(profile_url: str) -> dict:
    """Returns {shortCode, videoUrl, caption, ownerUsername, ...} for newest reel."""
    from apify_client import ApifyClient

    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        raise EnvironmentError("APIFY_API_TOKEN missing in .env")

    client = ApifyClient(token)
    run = client.actor("apify/instagram-scraper").call(
        run_input={
            "directUrls": [profile_url],
            "resultsType": "posts",
            "resultsLimit": 5,
            "onlyPostsNewerThan": "1 month",
        },
        timeout_secs=180,
    )
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    videos = [i for i in items if i.get("videoUrl")]
    if not videos:
        raise RuntimeError(f"Keine Reels auf {profile_url} in den letzten 30 Tagen")
    videos.sort(key=lambda i: i.get("timestamp", ""), reverse=True)
    return videos[0]


def download_video(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest)
    return dest
