# n8n Trading Images Library

Automated image library for trading assets with Azure Blob Storage hosting and n8n integration.

## 📋 Overview

This project provides a complete solution for:
- Fetching/generating 5 professional images for each trading asset
- Hosting images on Azure Blob Storage with public URLs
- Easy integration with n8n workflows via JSON mapping

## 🎯 Supported Assets

- **Cryptocurrencies**: Ethereum, BTC/USD, XRP
- **Forex Pairs**: EUR/USD, USD/CAD, GBP/USD, AUD
- **Commodities**: Gold

**Total**: 8 assets × 5 images = 40 professional trading images

## 🚀 Quick Start

### 1. Initial Setup

```bash
# Run the setup script
./setup.sh

# This will:
# - Create Python virtual environment
# - Install dependencies
# - Create .env file from template
```

### 2. Configure Environment Variables

Edit `.env` file with your credentials:

#### Option A: Free Images (Unsplash - Recommended)
```bash
# Get API key from: https://unsplash.com/developers
UNSPLASH_ACCESS_KEY=your_key_here
```

#### Option B: AI-Generated (Azure OpenAI DALL-E 3)
```bash
AZURE_OPENAI_ENDPOINT=https://brn-azai.openai.azure.com/
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_DALLE_DEPLOYMENT=dall-e-3
```

#### Azure Storage (Required for Both)
```bash
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
```

### 3. Fetch/Generate Images

#### Option A: Fetch from Unsplash (Free)
```bash
source venv/bin/activate
python3 fetch_images.py
```

#### Option B: Generate with DALL-E 3 (Paid)
```bash
source venv/bin/activate
python3 generate_with_dalle.py
```

### 4. Upload to Azure

```bash
python3 upload_to_azure.py
```

This will:
- Upload all images to Azure Blob Storage `$web` container
- Generate `image-urls.json` with all public URLs
- Display your image URLs

## 📁 Project Structure

```
n8n-trading-images/
├── ethereum/          # Ethereum images (5)
├── eur-usd/           # EUR/USD images (5)
├── btc-usd/           # BTC/USD images (5)
├── gold/              # Gold images (5)
├── xrp/               # XRP images (5)
├── usd-cad/           # USD/CAD images (5)
├── gbp-usd/           # GBP/USD images (5)
├── aud/               # AUD images (5)
├── config.json        # Asset configuration
├── fetch_images.py    # Unsplash fetcher
├── generate_with_dalle.py  # DALL-E generator
├── upload_to_azure.py # Azure uploader
├── image-urls.json    # Generated URL mapping
└── .env               # Your credentials
```

## 🔗 n8n Integration

### Method 1: Direct URL Access

Use the HTTP Request node in n8n:

```javascript
// Read the image-urls.json file
const imageUrls = {
  "ethereum": [
    "https://yourstorage.z6.web.core.windows.net/ethereum/ethereum-1.jpg",
    ...
  ],
  ...
};

// Get random image for asset
const asset = "ethereum";
const randomIndex = Math.floor(Math.random() * imageUrls[asset].length);
const imageUrl = imageUrls[asset][randomIndex];

return { imageUrl };
```

### Method 2: HTTP Request Node

1. Add HTTP Request node
2. Method: GET
3. URL: `https://yourstorage.z6.web.core.windows.net/{{$json["asset"]}}/{{$json["asset"]}}-1.jpg`
4. Use response in downstream nodes

### Method 3: JSON Lookup

1. Upload `image-urls.json` to your storage
2. Fetch JSON in n8n workflow
3. Lookup images by asset name

## ⚙️ Azure Setup Guide

### Create Storage Account

1. **Azure Portal** → **Storage Accounts** → **Create**
2. **Basics**:
   - Subscription: Your subscription
   - Resource Group: `AZAI_group`
   - Storage account name: Choose unique name (e.g., `n8ntradingimages`)
   - Region: Sweden Central
   - Performance: Standard
   - Redundancy: LRS (Locally-redundant)

3. **Review + Create** → **Create**

### Enable Static Website

1. Open your storage account
2. **Data management** → **Static website**
3. **Enable** static website
4. Index document: `index.html` (optional)
5. **Save**
6. Note the **Primary endpoint** URL

### Get Connection String

1. Storage account → **Access keys**
2. Click **Show** next to Connection string
3. Copy **Connection string** to `.env` file

### Update config.json

```json
{
  "azure": {
    "storage_account_name": "n8ntradingimages",  // ← Your account name
    ...
  }
}
```

## 🎨 Azure OpenAI DALL-E 3 Setup

### Required Resources

You already have Azure OpenAI at: `https://brn-azai.openai.azure.com/`

### Deploy DALL-E 3

1. **Azure OpenAI Studio** → **Deployments**
2. **Create new deployment**
3. Model: `dall-e-3`
4. Deployment name: `dall-e-3`
5. **Create**

### Get API Key

1. Azure OpenAI resource → **Keys and Endpoint**
2. Copy **Key 1** and **Endpoint**
3. Add to `.env` file

### Estimated Costs

- **Standard quality (1024x1024)**: ~$0.04 per image
- **HD quality (1024x1024)**: ~$0.08 per image
- **40 images total**: $1.60 - $3.20

## 🔑 Getting Unsplash API Key

1. Go to [unsplash.com/developers](https://unsplash.com/developers)
2. Click **Register as a developer**
3. Create new application
4. Copy **Access Key**
5. Add to `.env` file

**Rate Limits**: 50 requests/hour (free tier)

## 📝 Adding New Assets

1. **Edit `config.json`**:
```json
{
  "name": "oil",
  "folder": "oil",
  "search_terms": [
    "crude oil trading",
    "oil barrels",
    "oil price chart",
    "petroleum trading",
    "oil market"
  ],
  "images_per_asset": 5
}
```

2. **Create folder**:
```bash
mkdir oil
```

3. **Run fetcher/generator again**:
```bash
python3 fetch_images.py  # or generate_with_dalle.py
```

4. **Upload to Azure**:
```bash
python3 upload_to_azure.py
```

## 🛠️ Maintenance

### Replacing Images

1. Delete existing images locally
2. Run fetch/generate script again
3. Re-upload to Azure

### Checking Azure Storage

```bash
# List all blobs
az storage blob list \
  --account-name your-account \
  --container-name '$web' \
  --output table
```

### Backup Images

```bash
# Create backup
tar -czf trading-images-backup.tar.gz ethereum/ eur-usd/ btc-usd/ gold/ xrp/ usd-cad/ gbp-usd/ aud/
```

## 💰 Cost Estimates

### Unsplash Option
- API: **FREE** (50 requests/hour)
- Azure Storage: ~$0.02/GB/month
- Total for 40 images (~100MB): **~$0.002/month**

### DALL-E Option
- Image generation: $1.60 - $3.20 (one-time)
- Azure Storage: ~$0.02/GB/month
- Total: **~$2-3 one-time + $0.002/month**

## 🐛 Troubleshooting

### "UNSPLASH_ACCESS_KEY not found"
- Ensure `.env` file exists and contains the key
- Activate virtual environment: `source venv/bin/activate`

### "Azure Storage connection failed"
- Check connection string in `.env`
- Ensure storage account exists
- Verify static website is enabled

### "No images found for asset"
- Try different search terms in `config.json`
- Check Unsplash rate limits (50/hour)
- Use more specific search queries

### DALL-E "Deployment not found"
- Verify deployment name matches `.env`
- Check Azure OpenAI resource has DALL-E 3 deployed
- Wait 5-10 minutes after deployment

## 📚 Resources

- [Unsplash API Documentation](https://unsplash.com/documentation)
- [Azure Blob Storage Static Website](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-static-website)
- [Azure OpenAI DALL-E 3](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/dall-e)
- [n8n HTTP Request Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)

## 📄 License

MIT License - Free for personal and commercial use

## 🤝 Support

For issues or questions:
1. Check troubleshooting section
2. Review Azure Portal for service status
3. Verify all credentials in `.env`

---

**Made for n8n workflows** | **Powered by Azure** | **Images from Unsplash / DALL-E 3**
