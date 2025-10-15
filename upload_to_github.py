#!/usr/bin/env python3
"""
GitHub Upload Script for n8n Trading Images
Commits and pushes images to GitHub repository with proper URLs.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict

class GitHubUploader:
    def __init__(self, config_path: str = "config.json"):
        """Initialize GitHub uploader with configuration."""
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.base_dir = Path(__file__).parent
        self.github_user = "oded-be-z"
        self.repo_name = "n8n-trading-images"
        self.branch = "main"

    def git_command(self, command: list) -> tuple:
        """Execute git command."""
        try:
            result = subprocess.run(
                command,
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

    def check_git_status(self):
        """Check current git status."""
        success, output = self.git_command(['git', 'status', '--porcelain'])
        if success:
            if output.strip():
                print(f"📝 Git status:\n{output}")
                return True
            else:
                print("✓ No changes to commit")
                return False
        else:
            print(f"❌ Error checking git status: {output}")
            return False

    def commit_and_push(self):
        """Commit all changes and push to GitHub."""
        print("\n" + "="*60)
        print("📤 Committing and pushing to GitHub...")
        print("="*60)

        # Check if there are changes
        if not self.check_git_status():
            print("✓ Repository is up to date")
            return True

        # Add all files
        print("\n📝 Adding files to git...")
        success, output = self.git_command(['git', 'add', '.'])
        if not success:
            print(f"❌ Error adding files: {output}")
            return False
        print("✅ Files added")

        # Commit
        print("\n💾 Creating commit...")
        commit_message = "Add n8n trading images library with 40 professional images"
        success, output = self.git_command(['git', 'commit', '-m', commit_message])
        if not success:
            if "nothing to commit" in output:
                print("✓ Nothing to commit, working tree clean")
            else:
                print(f"❌ Error committing: {output}")
                return False
        else:
            print(f"✅ Commit created: {commit_message}")

        # Push to GitHub
        print("\n🚀 Pushing to GitHub...")
        success, output = self.git_command(['git', 'push', 'origin', self.branch])
        if not success:
            print(f"❌ Error pushing: {output}")
            return False

        print("✅ Successfully pushed to GitHub!")
        return True

    def generate_github_urls(self) -> Dict:
        """Generate GitHub raw URLs for all images."""
        url_mapping = {}

        # Base URL for raw GitHub content
        base_url = f"https://raw.githubusercontent.com/{self.github_user}/{self.repo_name}/{self.branch}"

        print("\n" + "="*60)
        print("🔗 Generating GitHub URLs...")
        print("="*60)

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
            print(f"  ✅ {asset_name}: {len(asset_urls)} URLs")

        # Save to JSON file
        output_path = self.base_dir / 'image-urls.json'
        with open(output_path, 'w') as f:
            json.dump(url_mapping, f, indent=2)

        print(f"\n📄 Generated: image-urls.json")
        return url_mapping

    def display_urls(self):
        """Display example URLs for accessing images."""
        base_url = f"https://raw.githubusercontent.com/{self.github_user}/{self.repo_name}/{self.branch}"

        print(f"\n🌐 Your images are now available at:")
        print(f"   {base_url}/[asset]/[filename].jpg")
        print(f"\n📋 Example URLs:")

        # Show first asset as example
        first_asset = self.config['assets'][0]
        folder = first_asset['folder']
        print(f"   {base_url}/{folder}/{folder}-1.jpg")
        print(f"   {base_url}/{folder}/{folder}-2.jpg")
        print(f"   ...")

        print(f"\n🔗 GitHub Repository:")
        print(f"   https://github.com/{self.github_user}/{self.repo_name}")

        print(f"\n📄 All URLs saved in: image-urls.json")


def main():
    """Main entry point."""
    try:
        uploader = GitHubUploader()

        # Commit and push to GitHub
        if not uploader.commit_and_push():
            print("\n❌ Upload failed!")
            return 1

        # Generate GitHub URLs
        uploader.generate_github_urls()

        # Display URLs
        uploader.display_urls()

        print("\n" + "="*60)
        print("✨ GitHub Upload Complete!")
        print("="*60)
        print("\n✅ Next steps:")
        print("   1. Visit: https://github.com/oded-be-z/n8n-trading-images")
        print("   2. Verify images are uploaded")
        print("   3. Use image-urls.json in your n8n workflow")
        print("")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
