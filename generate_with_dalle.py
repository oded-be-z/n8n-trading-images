#!/usr/bin/env python3
"""
DALL-E 3 Image Generator for Trading Assets
Generates custom AI images using Azure OpenAI DALL-E 3.
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict
import time

class DalleImageGenerator:
    def __init__(self, config_path: str = "config.json"):
        """Initialize DALL-E generator with configuration."""
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # Azure OpenAI credentials
        self.azure_endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
        self.azure_api_key = os.environ.get('AZURE_OPENAI_API_KEY')
        self.deployment_name = os.environ.get('AZURE_OPENAI_DALLE_DEPLOYMENT', 'dall-e-3')

        if not self.azure_endpoint or not self.azure_api_key:
            raise ValueError(
                "Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY environment variables\n"
                "Example: export AZURE_OPENAI_ENDPOINT='https://brn-azai.openai.azure.com/'\n"
                "Example: export AZURE_OPENAI_API_KEY='your-api-key'"
            )

        self.base_dir = Path(__file__).parent

        # DALL-E 3 prompts for each asset type
        self.prompts = {
            "ethereum": [
                "Professional financial chart showing Ethereum cryptocurrency price trends, modern blue and purple colors, high quality digital art",
                "Ethereum coin glowing with blockchain network connections, futuristic technology theme, professional trading background",
                "Stock market screen displaying Ethereum ETH price graph with candlesticks, professional finance photography",
                "Abstract representation of Ethereum blockchain network with glowing nodes and connections, deep purple and blue gradient",
                "Professional trader's desk with multiple monitors showing Ethereum charts and trading interface, modern office setting"
            ],
            "eur_usd": [
                "Professional forex trading chart showing EUR/USD currency pair, candlestick patterns, modern financial interface",
                "Euro and US Dollar symbols with rising arrow graph, professional financial concept, clean design",
                "Trading screen with EUR/USD exchange rate chart, professional forex trading platform interface",
                "European and American flags with financial charts overlay, professional business photography",
                "Modern financial chart showing Euro to Dollar exchange rate trends, professional blue theme"
            ],
            "btc_usd": [
                "Bitcoin BTC cryptocurrency chart with candlestick patterns, professional trading screen, golden and black theme",
                "Golden Bitcoin coin on financial chart background, professional cryptocurrency trading concept",
                "Professional trading terminal showing BTC/USD price movements with technical indicators",
                "Bitcoin symbol with upward trending graph lines, modern financial technology concept",
                "Multiple cryptocurrency trading screens focused on Bitcoin price action, professional trader setup"
            ],
            "gold": [
                "Gold bars stacked with financial price chart overlay, professional commodity trading concept",
                "Professional gold price chart with candlestick patterns, warm golden colors, trading interface",
                "Shiny gold bullion with rising price graph in background, professional investment photography",
                "Gold commodity trading screen showing price movements and technical analysis, professional interface",
                "Abstract golden waves representing gold price fluctuations, professional financial art"
            ],
            "xrp": [
                "Ripple XRP cryptocurrency coin with blockchain network visualization, professional blue theme",
                "XRP price chart with technical indicators, professional cryptocurrency trading interface",
                "Ripple logo with financial graph overlay showing price trends, modern digital design",
                "Trading screen displaying XRP cryptocurrency price movements, professional trading platform",
                "Ripple XRP digital currency concept with network connections, futuristic blue color scheme"
            ],
            "usd_cad": [
                "USD/CAD forex pair chart with candlestick patterns, professional trading interface",
                "US and Canadian flags with financial chart overlay, professional currency trading concept",
                "Professional forex terminal showing USD to CAD exchange rate movements",
                "Modern financial chart displaying US Dollar to Canadian Dollar trends, clean interface",
                "Trading screen with USD/CAD currency pair analysis and technical indicators"
            ],
            "gbp_usd": [
                "GBP/USD cable forex chart with professional trading interface, British and American theme",
                "British Pound and US Dollar symbols with rising trend graph, professional financial concept",
                "Professional forex trading screen showing GBP/USD price movements and patterns",
                "UK and US flags with financial chart overlay, professional currency trading visualization",
                "Cable pair GBP/USD candlestick chart with technical analysis, professional trading platform"
            ],
            "aud": [
                "Australian Dollar AUD forex chart with professional trading interface, green and gold theme",
                "AUD currency symbol with rising financial graph, professional Australian dollar trading concept",
                "Professional trading terminal showing Australian Dollar exchange rates and trends",
                "AUD/USD currency pair chart with technical indicators, professional forex platform",
                "Australian flag with financial market chart overlay, professional currency trading visualization"
            ]
        }

    def generate_image(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> str:
        """Generate a single image using DALL-E 3."""
        api_version = "2024-02-01"
        url = f"{self.azure_endpoint}/openai/deployments/{self.deployment_name}/images/generations?api-version={api_version}"

        headers = {
            "api-key": self.azure_api_key,
            "Content-Type": "application/json"
        }

        data = {
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "style": "natural",  # or "vivid" for more hyper-real images
            "n": 1
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        image_url = result['data'][0]['url']

        return image_url

    def download_image(self, image_url: str, save_path: Path) -> bool:
        """Download generated image from URL."""
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return True
        except Exception as e:
            print(f"❌ Error downloading image: {e}")
            return False

    def generate_all_images(self):
        """Generate all images using DALL-E 3."""
        print("🎨 Starting DALL-E 3 image generation...")
        print(f"🤖 Azure OpenAI Endpoint: {self.azure_endpoint}")
        print(f"📊 Total assets: {len(self.config['assets'])}")
        print(f"🎯 Images per asset: 5")

        total_generated = 0
        total_cost_estimate = 0.0

        for asset in self.config['assets']:
            asset_name = asset['name']
            folder = asset['folder']
            images_per_asset = 5

            print(f"\n{'='*60}")
            print(f"🎨 Generating: {asset_name.upper()}")
            print(f"{'='*60}")

            # Create folder if it doesn't exist
            asset_folder = self.base_dir / folder
            asset_folder.mkdir(exist_ok=True)

            # Get prompts for this asset
            prompts = self.prompts.get(asset_name, [])

            # Generate images
            for i, prompt in enumerate(prompts[:images_per_asset]):
                image_filename = f"{folder}-{i+1}.jpg"
                image_path = asset_folder / image_filename

                # Skip if image already exists
                if image_path.exists():
                    print(f"  ✓ Skipped: {image_filename} (already exists)")
                    total_generated += 1
                    continue

                print(f"  🎨 Generating {i+1}/5...", end=" ")

                try:
                    # Generate image
                    image_url = self.generate_image(prompt, size="1024x1024", quality="standard")

                    # Download image
                    if self.download_image(image_url, image_path):
                        print(f"✅ Generated: {image_filename}")
                        total_generated += 1
                        total_cost_estimate += 0.04  # Approximate cost per image
                    else:
                        print(f"❌ Failed to download")

                    # Rate limiting: Be respectful with API calls
                    time.sleep(2)

                except Exception as e:
                    print(f"❌ Error: {e}")

        print(f"\n{'='*60}")
        print(f"✨ Generation Complete!")
        print(f"🎨 Generated: {total_generated} images")
        print(f"💰 Estimated Cost: ${total_cost_estimate:.2f} USD")
        print(f"{'='*60}")


def main():
    """Main entry point."""
    try:
        generator = DalleImageGenerator()

        # Generate all images
        generator.generate_all_images()

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
