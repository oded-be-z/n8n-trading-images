#!/usr/bin/env python3
"""
Azure Blob Storage Upload Script
Uploads trading images to Azure Blob Storage with static website hosting.
"""

import os
import json
from pathlib import Path
from azure.storage.blob import BlobServiceClient, ContentSettings
from typing import Dict

class AzureBlobUploader:
    def __init__(self, config_path: str = "config.json"):
        """Initialize the Azure uploader with configuration."""
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # Get Azure Storage connection string from environment
        self.connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        if not self.connection_string:
            raise ValueError("Please set AZURE_STORAGE_CONNECTION_STRING environment variable")

        self.storage_account_name = self.config['azure']['storage_account_name']
        self.container_name = self.config['azure']['container_name']

        # Initialize blob service client
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

        self.base_dir = Path(__file__).parent

    def create_container_if_not_exists(self):
        """Create the $web container if it doesn't exist."""
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            if not container_client.exists():
                container_client.create_container()
                print(f"✅ Created container: {self.container_name}")
            else:
                print(f"✓ Container already exists: {self.container_name}")
        except Exception as e:
            print(f"❌ Error creating container: {e}")

    def upload_image(self, local_path: Path, blob_name: str) -> bool:
        """Upload a single image to Azure Blob Storage."""
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )

            # Set content type for images
            content_settings = ContentSettings(content_type='image/jpeg')

            # Upload the file
            with open(local_path, 'rb') as data:
                blob_client.upload_blob(
                    data,
                    overwrite=True,
                    content_settings=content_settings
                )

            return True
        except Exception as e:
            print(f"❌ Error uploading {blob_name}: {e}")
            return False

    def upload_all_images(self):
        """Upload all images to Azure Blob Storage."""
        print("☁️  Starting Azure Blob Storage upload...")
        print(f"📦 Storage Account: {self.storage_account_name}")
        print(f"📁 Container: {self.container_name}")

        # Ensure container exists
        self.create_container_if_not_exists()

        total_uploaded = 0
        total_skipped = 0

        for asset in self.config['assets']:
            folder = asset['folder']
            images_per_asset = asset['images_per_asset']

            print(f"\n{'='*60}")
            print(f"📁 Uploading: {folder.upper()}")
            print(f"{'='*60}")

            asset_folder = self.base_dir / folder

            # Upload each image
            for i in range(1, images_per_asset + 1):
                image_filename = f"{folder}-{i}.jpg"
                local_path = asset_folder / image_filename

                if not local_path.exists():
                    print(f"  ⚠️  Skipped: {image_filename} (file not found)")
                    total_skipped += 1
                    continue

                # Blob name includes folder structure
                blob_name = f"{folder}/{image_filename}"

                print(f"  ☁️  Uploading: {blob_name}...", end=" ")

                if self.upload_image(local_path, blob_name):
                    print("✅ Done")
                    total_uploaded += 1
                else:
                    total_skipped += 1

        print(f"\n{'='*60}")
        print(f"✨ Upload Complete!")
        print(f"📤 Uploaded: {total_uploaded} images")
        print(f"⏭️  Skipped: {total_skipped} images")
        print(f"{'='*60}")

        # Generate and display URLs
        self.display_access_urls()

    def display_access_urls(self):
        """Display the static website URL for accessing images."""
        base_url = f"https://{self.storage_account_name}.z6.web.core.windows.net"

        print(f"\n🌐 Your images are now available at:")
        print(f"   {base_url}/")
        print(f"\nExample URLs:")

        # Show first asset as example
        first_asset = self.config['assets'][0]
        folder = first_asset['folder']
        print(f"   {base_url}/{folder}/{folder}-1.jpg")
        print(f"   {base_url}/{folder}/{folder}-2.jpg")
        print(f"   ...")

    def generate_url_mapping(self) -> Dict:
        """Generate complete URL mapping for all images."""
        url_mapping = {}
        base_url = f"https://{self.storage_account_name}.z6.web.core.windows.net"

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
        print(f"🔗 Ready for n8n integration!")

        return url_mapping


def main():
    """Main entry point."""
    try:
        uploader = AzureBlobUploader()

        # Upload all images
        uploader.upload_all_images()

        # Generate URL mapping
        uploader.generate_url_mapping()

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
