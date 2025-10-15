#!/usr/bin/env python3
"""
n8n Trading Images Fetcher
Fetches high-quality trading images from Unsplash API and organizes them for n8n workflows.
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict, List
import time

class TradingImagesFetcher:
    def __init__(self, config_path: str = "config.json"):
        """Initialize the fetcher with configuration."""
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.unsplash_api_key = os.environ.get('UNSPLASH_ACCESS_KEY')
        if not self.unsplash_api_key:
            raise ValueError("Please set UNSPLASH_ACCESS_KEY environment variable")

        self.base_dir = Path(__file__).parent
        self.headers = {
            'Authorization': f'Client-ID {self.unsplash_api_key}'
        }

    def fetch_image(self, search_term: str, page: int = 1) -> Dict:
        """Fetch a single image from Unsplash based on search term."""
        url = f"{self.config['unsplash']['api_url']}/search/photos"
        params = {
            'query': search_term,
            'page': page,
            'per_page': self.config['unsplash']['per_page'],
            'orientation': self.config['unsplash']['orientation']
        }

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        data = response.json()
        if data['total'] > 0:
            return data['results'][0]
        return None

    def download_image(self, image_data: Dict, save_path: Path) -> bool:
        """Download image from Unsplash and save to disk."""
        try:
            # Use regular quality (not raw) to save bandwidth
            image_url = image_data['urls']['regular']

            # Download image
            response = requests.get(image_url, stream=True)
            response.raise_for_status()

            # Save image
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Trigger download tracking for Unsplash (required by API guidelines)
            if 'links' in image_data and 'download_location' in image_data['links']:
                requests.get(image_data['links']['download_location'], headers=self.headers)

            return True
        except Exception as e:
            print(f"Error downloading image: {e}")
            return False

    def fetch_all_images(self):
        """Fetch all images for all assets."""
        print("🖼️  Starting to fetch trading images from Unsplash...")
        print(f"📊 Total assets: {len(self.config['assets'])}")
        print(f"🎯 Images per asset: {self.config['assets'][0]['images_per_asset']}")

        total_images = 0

        for asset in self.config['assets']:
            asset_name = asset['name']
            folder = asset['folder']
            search_terms = asset['search_terms']
            images_per_asset = asset['images_per_asset']

            print(f"\n{'='*60}")
            print(f"📁 Processing: {asset_name.upper()}")
            print(f"{'='*60}")

            # Create folder if it doesn't exist
            asset_folder = self.base_dir / folder
            asset_folder.mkdir(exist_ok=True)

            # Fetch images using different search terms
            for i, search_term in enumerate(search_terms[:images_per_asset]):
                image_filename = f"{folder}-{i+1}.jpg"
                image_path = asset_folder / image_filename

                # Skip if image already exists
                if image_path.exists():
                    print(f"  ✓ Skipped: {image_filename} (already exists)")
                    total_images += 1
                    continue

                print(f"  🔍 Searching: {search_term}...", end=" ")

                try:
                    # Fetch image data
                    image_data = self.fetch_image(search_term, page=1)

                    if image_data:
                        # Download image
                        if self.download_image(image_data, image_path):
                            print(f"✅ Downloaded: {image_filename}")
                            total_images += 1
                        else:
                            print(f"❌ Failed to download")
                    else:
                        print(f"❌ No results found")

                    # Rate limiting: Unsplash allows 50 requests per hour
                    time.sleep(1)  # Be nice to the API

                except Exception as e:
                    print(f"❌ Error: {e}")

        print(f"\n{'='*60}")
        print(f"✨ Complete! Downloaded {total_images} images")
        print(f"{'='*60}")

    def generate_url_mapping(self, storage_account_name: str) -> Dict:
        """Generate URL mapping for n8n integration."""
        url_mapping = {}

        base_url = f"https://{storage_account_name}.z6.web.core.windows.net"

        for asset in self.config['assets']:
            asset_name = asset['name']
            folder = asset['folder']
            images_per_asset = asset['images_per_asset']

            asset_urls = []
            for i in range(1, images_per_asset + 1):
                image_filename = f"{folder}-{i}.jpg"
                url = f"{base_url}/{folder}/{image_filename}"
                asset_urls.append(url)

            url_mapping[asset_name] = asset_urls

        # Save to JSON file
        output_path = self.base_dir / 'image-urls.json'
        with open(output_path, 'w') as f:
            json.dump(url_mapping, f, indent=2)

        print(f"\n📄 Generated: image-urls.json")
        print(f"🔗 URLs ready for n8n integration!")

        return url_mapping


def main():
    """Main entry point."""
    try:
        fetcher = TradingImagesFetcher()

        # Fetch all images
        fetcher.fetch_all_images()

        # Generate URL mapping (you'll update storage account name after Azure setup)
        print("\n" + "="*60)
        print("Note: Update storage_account_name in config.json before generating URLs")
        print("="*60)

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
