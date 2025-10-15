#!/usr/bin/env python3
"""
Retry fetching missing images with simpler search terms to avoid rate limits.
"""

import os
import json
import requests
from pathlib import Path
import time

UNSPLASH_ACCESS_KEY = "TuUN__xCUdR6_gk1JBRVKlc9M_FSBbETc_uylmpxo-A"

# Simple, generic search terms that work better
missing_images = {
    "eur-usd": [("forex trading", "eur-usd-2.jpg")],
    "xrp": [("cryptocurrency", "xrp-4.jpg")],
    "usd-cad": [
        ("canadian money", "usd-cad-1.jpg"),
        ("currency exchange", "usd-cad-3.jpg"),
        ("forex chart", "usd-cad-4.jpg"),
        ("trading screen", "usd-cad-5.jpg")
    ],
    "gbp-usd": [
        ("british pound", "gbp-usd-1.jpg"),
        ("currency trading", "gbp-usd-2.jpg"),
        ("forex market", "gbp-usd-3.jpg"),
        ("stock exchange", "gbp-usd-4.jpg"),
        ("financial chart", "gbp-usd-5.jpg")
    ],
    "aud": [
        ("australian currency", "aud-1.jpg"),
        ("money exchange", "aud-2.jpg"),
        ("trading floor", "aud-3.jpg"),
        ("currency rates", "aud-4.jpg"),
        ("financial graph", "aud-5.jpg")
    ]
}

def fetch_image(search_term: str) -> dict:
    """Fetch image from Unsplash."""
    url = "https://api.unsplash.com/search/photos"
    headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
    params = {
        'query': search_term,
        'page': 1,
        'per_page': 1,
        'orientation': 'landscape'
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    if data['total'] > 0:
        return data['results'][0]
    return None

def download_image(image_data: dict, save_path: Path) -> bool:
    """Download image."""
    try:
        image_url = image_data['urls']['regular']
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Trigger download tracking
        if 'links' in image_data and 'download_location' in image_data['links']:
            headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
            requests.get(image_data['links']['download_location'], headers=headers)

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

print("🔄 Retrying missing images with simpler search terms...")
print("⏰ Using 3-second delays to avoid rate limits\n")

total_downloaded = 0

for folder, images in missing_images.items():
    print(f"📁 {folder.upper()}")
    folder_path = Path(folder)
    folder_path.mkdir(exist_ok=True)

    for search_term, filename in images:
        filepath = folder_path / filename

        if filepath.exists():
            print(f"  ✓ {filename} already exists")
            continue

        print(f"  🔍 {search_term}...", end=" ")

        try:
            image_data = fetch_image(search_term)
            if image_data:
                if download_image(image_data, filepath):
                    print(f"✅ {filename}")
                    total_downloaded += 1
                else:
                    print(f"❌ Download failed")
            else:
                print(f"❌ No results")

            # Important: 3 second delay between requests
            time.sleep(3)

        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(3)

    print()

print(f"✨ Downloaded {total_downloaded} additional images!")
