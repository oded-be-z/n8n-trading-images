# n8n Trading Images Integration Guide
**For AI Coding Agents & Developers**

## Overview
This document explains how to integrate 40 professional trading images hosted on GitHub into n8n workflows. Each trading asset has 5 high-quality images available via direct URLs.

---

## Image Repository Structure

### GitHub Repository
- **URL**: https://github.com/oded-be-z/n8n-trading-images
- **Branch**: main
- **Total Images**: 40 (8 assets × 5 images each)
- **Format**: JPG
- **Hosting**: GitHub raw content (free, permanent URLs)

### Assets Available
| Asset Name | Folder Name | Image Count | Description |
|------------|-------------|-------------|-------------|
| Ethereum | `ethereum` | 5 | Ethereum cryptocurrency images |
| Bitcoin/USD | `btc-usd` | 5 | Bitcoin trading images |
| EUR/USD | `eur-usd` | 5 | Euro/Dollar forex pair |
| Gold | `gold` | 5 | Gold commodity trading |
| Ripple XRP | `xrp` | 5 | XRP cryptocurrency |
| USD/CAD | `usd-cad` | 5 | US Dollar/Canadian Dollar |
| GBP/USD | `gbp-usd` | 5 | British Pound/US Dollar |
| Australian Dollar | `aud` | 5 | Australian Dollar forex |

---

## URL Structure

### Pattern
```
https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/{FOLDER}/{FOLDER}-{NUMBER}.jpg
```

### Variables
- `{FOLDER}`: Asset folder name (lowercase, hyphenated)
- `{NUMBER}`: Image number (1-5)

### Examples
```
https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/ethereum/ethereum-1.jpg
https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/btc-usd/btc-usd-3.jpg
https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/gold/gold-5.jpg
```

---

## Asset Name Mapping

### JSON Key to Folder Mapping
```json
{
  "ethereum": "ethereum",
  "btc_usd": "btc-usd",
  "eur_usd": "eur-usd",
  "gold": "gold",
  "xrp": "xrp",
  "usd_cad": "usd-cad",
  "gbp_usd": "gbp-usd",
  "aud": "aud"
}
```

### Common Asset Name Variations
Handle these input variations in your n8n flow:

| User Input | Maps To Folder | Example URL |
|------------|----------------|-------------|
| `ethereum`, `ETH`, `Ethereum` | `ethereum` | `.../ethereum/ethereum-1.jpg` |
| `bitcoin`, `BTC`, `BTC/USD` | `btc-usd` | `.../btc-usd/btc-usd-1.jpg` |
| `EUR/USD`, `EURUSD`, `euro` | `eur-usd` | `.../eur-usd/eur-usd-1.jpg` |
| `gold`, `GOLD`, `XAU` | `gold` | `.../gold/gold-1.jpg` |
| `ripple`, `XRP`, `Ripple` | `xrp` | `.../xrp/xrp-1.jpg` |
| `USD/CAD`, `USDCAD` | `usd-cad` | `.../usd-cad/usd-cad-1.jpg` |
| `GBP/USD`, `GBPUSD`, `cable` | `gbp-usd` | `.../gbp-usd/gbp-usd-1.jpg` |
| `AUD`, `aussie`, `AUD/USD` | `aud` | `.../aud/aud-1.jpg` |

---

## n8n Integration Methods

### Method 1: Dynamic URL Construction (Recommended)

**Use Case**: When you have asset name as variable in your workflow

**n8n Expression**:
```javascript
{{ "https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/" + $json.asset_folder + "/" + $json.asset_folder + "-" + (Math.floor(Math.random() * 5) + 1) + ".jpg" }}
```

**Example Data**:
```json
{
  "asset_folder": "ethereum",
  "asset_name": "Ethereum"
}
```

**Result**: Random image from `ethereum-1.jpg` to `ethereum-5.jpg`

---

### Method 2: Direct URL Template

**Use Case**: When asset is known at workflow design time

**HTTP Request Node Settings**:
- Method: `GET`
- URL: `https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/{{$json["asset"]}}/{{$json["asset"]}}-1.jpg`

**Input Example**:
```json
{
  "asset": "btc-usd",
  "title": "Bitcoin Analysis"
}
```

**Output**: Direct image URL for Bitcoin

---

### Method 3: Complete URL Mapping (Best for Complex Flows)

**Step 1**: Fetch complete URL mapping
- HTTP Request Node
- Method: `GET`
- URL: `https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/image-urls.json`

**Response Structure**:
```json
{
  "ethereum": [
    "https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/ethereum/ethereum-1.jpg",
    "https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/ethereum/ethereum-2.jpg",
    "https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/ethereum/ethereum-3.jpg",
    "https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/ethereum/ethereum-4.jpg",
    "https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/ethereum/ethereum-5.jpg"
  ],
  "btc_usd": [...],
  "gold": [...]
}
```

**Step 2**: Access in subsequent nodes
```javascript
// Get first image for ethereum
{{ $json.ethereum[0] }}

// Get random image for ethereum
{{ $json.ethereum[Math.floor(Math.random() * $json.ethereum.length)] }}

// Get specific image (3rd image)
{{ $json.ethereum[2] }}
```

---

## Complete n8n Function Node Example

### Asset Name Normalizer + URL Generator

```javascript
// Input: { "asset": "Bitcoin", "title": "BTC Analysis" }
// Output: Direct image URL

// Normalization mapping
const assetMap = {
  'ethereum': 'ethereum',
  'eth': 'ethereum',
  'bitcoin': 'btc-usd',
  'btc': 'btc-usd',
  'btc/usd': 'btc-usd',
  'eur/usd': 'eur-usd',
  'eurusd': 'eur-usd',
  'euro': 'eur-usd',
  'gold': 'gold',
  'xau': 'gold',
  'xrp': 'xrp',
  'ripple': 'xrp',
  'usd/cad': 'usd-cad',
  'usdcad': 'usd-cad',
  'gbp/usd': 'gbp-usd',
  'gbpusd': 'gbp-usd',
  'cable': 'gbp-usd',
  'aud': 'aud',
  'aud/usd': 'aud',
  'audusd': 'aud',
  'aussie': 'aud'
};

// Get asset name from input and normalize
const inputAsset = $input.item.json.asset.toLowerCase().trim();
const folder = assetMap[inputAsset] || 'ethereum'; // Default to ethereum

// Generate random image number (1-5)
const imageNumber = Math.floor(Math.random() * 5) + 1;

// Construct URL
const imageUrl = `https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/${folder}/${folder}-${imageNumber}.jpg`;

// Return result
return {
  json: {
    asset: $input.item.json.asset,
    asset_folder: folder,
    image_url: imageUrl,
    image_number: imageNumber,
    title: $input.item.json.title || `${folder} trading`
  }
};
```

**Input Example**:
```json
{
  "asset": "Bitcoin",
  "title": "BTC Market Analysis"
}
```

**Output Example**:
```json
{
  "asset": "Bitcoin",
  "asset_folder": "btc-usd",
  "image_url": "https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/btc-usd/btc-usd-3.jpg",
  "image_number": 3,
  "title": "BTC Market Analysis"
}
```

---

## n8n Code Node - Get Specific Image

### Get First Image for Asset
```javascript
const asset = $input.item.json.asset_name; // e.g., "ethereum"
const imageUrl = `https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/${asset}/${asset}-1.jpg`;

return {
  json: {
    image_url: imageUrl
  }
};
```

### Get Random Image for Asset
```javascript
const asset = $input.item.json.asset_name; // e.g., "gold"
const randomNum = Math.floor(Math.random() * 5) + 1;
const imageUrl = `https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/${asset}/${asset}-${randomNum}.jpg`;

return {
  json: {
    image_url: imageUrl,
    image_number: randomNum
  }
};
```

### Get All 5 Images for Asset
```javascript
const asset = $input.item.json.asset_name; // e.g., "xrp"
const baseUrl = "https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main";

const images = [];
for (let i = 1; i <= 5; i++) {
  images.push(`${baseUrl}/${asset}/${asset}-${i}.jpg`);
}

return {
  json: {
    asset: asset,
    images: images,
    count: images.length
  }
};
```

---

## Advanced: Rotation Strategy

### Round-Robin Image Selection
Store counter in workflow static data or database:

```javascript
// Assuming you have a counter stored somewhere
const asset = $input.item.json.asset_name;
let counter = $input.item.json.image_counter || 1;

// Construct URL
const imageUrl = `https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/${asset}/${asset}-${counter}.jpg`;

// Increment counter (1-5, then loop back)
const nextCounter = (counter % 5) + 1;

return {
  json: {
    image_url: imageUrl,
    image_counter: counter,
    next_counter: nextCounter
  }
};
```

---

## Error Handling

### Fallback to Default Image
```javascript
const assetMap = {
  'ethereum': 'ethereum',
  'btc': 'btc-usd',
  // ... other mappings
};

const inputAsset = ($input.item.json.asset || 'ethereum').toLowerCase();
const folder = assetMap[inputAsset] || 'ethereum'; // Fallback to ethereum
const imageNumber = Math.floor(Math.random() * 5) + 1;

const imageUrl = `https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/${folder}/${folder}-${imageNumber}.jpg`;

return {
  json: {
    image_url: imageUrl,
    fallback_used: !assetMap[inputAsset]
  }
};
```

---

## Testing URLs

### Quick Test in Browser
Open these URLs directly to verify images load:

```
https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/ethereum/ethereum-1.jpg
https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/gold/gold-3.jpg
https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/btc-usd/btc-usd-5.jpg
```

### Test in n8n HTTP Request Node
- Method: GET
- URL: `https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/ethereum/ethereum-1.jpg`
- Response Format: Binary
- Output Binary Data: Yes

---

## Complete Workflow Example

### Scenario: Trading Signal with Relevant Image

**Flow**:
1. **Webhook/Trigger**: Receive trading signal
   ```json
   {
     "signal": "BUY",
     "asset": "Bitcoin",
     "price": 45000
   }
   ```

2. **Function Node**: Normalize asset and generate image URL
   ```javascript
   const assetMap = { 'bitcoin': 'btc-usd', 'btc': 'btc-usd' };
   const asset = $input.item.json.asset.toLowerCase();
   const folder = assetMap[asset] || asset;
   const imgNum = Math.floor(Math.random() * 5) + 1;
   const imageUrl = `https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/${folder}/${folder}-${imgNum}.jpg`;

   return {
     json: {
       ...$input.item.json,
       image_url: imageUrl,
       asset_folder: folder
     }
   };
   ```

3. **HTTP Request Node**: Fetch image (optional)
   - URL: `{{ $json.image_url }}`
   - Response Format: Binary

4. **Send Notification** (Telegram/Email/Slack)
   - Message: `{{ $json.signal }} signal for {{ $json.asset }} at ${{ $json.price }}`
   - Image: `{{ $json.image_url }}`

---

## Performance & Caching

### CDN Behavior
- GitHub raw content is cached globally
- First load: ~200-500ms
- Subsequent loads: ~50-100ms (cached)
- No rate limits for public repos

### Best Practices
1. **Cache URLs locally** if using same asset repeatedly
2. **Batch fetch** if need multiple images
3. **Use random selection** to distribute load across 5 images per asset

---

## Maintenance

### Adding New Assets
If new assets are added to the repository, update your mapping:

```javascript
const assetMap = {
  // Existing
  'ethereum': 'ethereum',
  'btc': 'btc-usd',
  // New asset
  'silver': 'silver', // If silver folder is added
  'oil': 'crude-oil'  // If crude-oil folder is added
};
```

### Updating Images
Images can be updated in GitHub without changing URLs. n8n will automatically fetch the latest version.

---

## Summary for AI Agents

**Quick Implementation Checklist**:
- ✅ Asset names map to folder names (use mapping table above)
- ✅ Each folder has exactly 5 images: `{folder}-1.jpg` to `{folder}-5.jpg`
- ✅ URL pattern: `https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/{folder}/{folder}-{1-5}.jpg`
- ✅ Use random number (1-5) for variety
- ✅ Normalize input asset names (case-insensitive, handle variations)
- ✅ Default to `ethereum` if asset not found
- ✅ Images are JPEG format, publicly accessible, no authentication needed

**Integration Points**:
1. HTTP Request nodes → direct URL access
2. Function nodes → dynamic URL construction
3. Code nodes → advanced logic and rotation
4. Binary data handling → for downloading/attaching images

---

## Support & Updates

- **Repository**: https://github.com/oded-be-z/n8n-trading-images
- **Complete URL List**: https://raw.githubusercontent.com/oded-be-z/n8n-trading-images/main/image-urls.json
- **Issues**: Create issue in GitHub repo if images don't load

**Last Updated**: October 15, 2025
