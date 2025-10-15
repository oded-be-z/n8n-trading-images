#!/usr/bin/env python3
"""Fill missing image slots by duplicating existing similar images."""

import shutil
from pathlib import Path

# Map of what to copy to fill missing slots
duplicates = {
    "eur-usd/eur-usd-2.jpg": "eur-usd/eur-usd-1.jpg",  # Duplicate EUR/USD image
    "xrp/xrp-4.jpg": "xrp/xrp-1.jpg",  # Duplicate XRP image
    "usd-cad/usd-cad-1.jpg": "eur-usd/eur-usd-1.jpg",  # Use forex image
    "usd-cad/usd-cad-3.jpg": "eur-usd/eur-usd-3.jpg",  # Use forex image
    "usd-cad/usd-cad-4.jpg": "eur-usd/eur-usd-4.jpg",  # Use forex image
    "usd-cad/usd-cad-5.jpg": "eur-usd/eur-usd-5.jpg",  # Use forex image
    "gbp-usd/gbp-usd-1.jpg": "eur-usd/eur-usd-1.jpg",  # Use forex image
    "gbp-usd/gbp-usd-2.jpg": "eur-usd/eur-usd-3.jpg",  # Use forex image
    "gbp-usd/gbp-usd-3.jpg": "eur-usd/eur-usd-4.jpg",  # Use forex image
    "gbp-usd/gbp-usd-4.jpg": "eur-usd/eur-usd-5.jpg",  # Use forex image
    "gbp-usd/gbp-usd-5.jpg": "eur-usd/eur-usd-1.jpg",  # Use forex image
    "aud/aud-1.jpg": "eur-usd/eur-usd-1.jpg",  # Use forex image
    "aud/aud-2.jpg": "eur-usd/eur-usd-3.jpg",  # Use forex image
    "aud/aud-3.jpg": "eur-usd/eur-usd-4.jpg",  # Use forex image
    "aud/aud-4.jpg": "eur-usd/eur-usd-5.jpg",  # Use forex image
    "aud/aud-5.jpg": "eur-usd/eur-usd-1.jpg",  # Use forex image
}

print("📋 Filling missing image slots...")
filled = 0

for dest, src in duplicates.items():
    dest_path = Path(dest)
    src_path = Path(src)
    
    if not dest_path.exists() and src_path.exists():
        shutil.copy2(src_path, dest_path)
        print(f"  ✅ Created {dest}")
        filled += 1

print(f"\n✨ Filled {filled} missing slots!")
