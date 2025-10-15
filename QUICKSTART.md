# 🚀 Quick Start Guide - n8n Trading Images

## ⚡ 5-Minute Setup

### Step 1: Run Setup (30 seconds)
```bash
cd n8n-trading-images
./setup.sh
```

### Step 2: Choose Your Image Source

#### 🆓 Option A: Free Images (Recommended)
1. Go to [unsplash.com/developers](https://unsplash.com/developers)
2. Register → Create New App → Copy **Access Key**
3. Edit `.env`:
```bash
UNSPLASH_ACCESS_KEY=paste_your_key_here
```

#### 🤖 Option B: AI-Generated ($2-3 total)
Already have Azure OpenAI? Skip to credentials:
```bash
AZURE_OPENAI_ENDPOINT=https://brn-azai.openai.azure.com/
AZURE_OPENAI_API_KEY=paste_your_key_here
AZURE_OPENAI_DALLE_DEPLOYMENT=dall-e-3
```

### Step 3: Setup Azure Storage (2 minutes)

1. **Azure Portal** → **Storage Accounts** → **Create**
   - Name: `n8ntradingimg` (or any unique name)
   - Resource Group: `AZAI_group`
   - Region: `Sweden Central`
   - Redundancy: `LRS`
   - **Create**

2. **Enable Static Website**:
   - Storage Account → **Static website** → **Enable**
   - Save

3. **Get Connection String**:
   - **Access keys** → Show → Copy **Connection string**

4. **Update `.env`**:
```bash
AZURE_STORAGE_CONNECTION_STRING=paste_here
```

5. **Update `config.json`**:
```json
{
  "azure": {
    "storage_account_name": "n8ntradingimg"  // ← Your account name
  }
}
```

### Step 4: Generate Images (2 minutes)

#### For Unsplash (Free):
```bash
source venv/bin/activate
python3 fetch_images.py
```

#### For DALL-E 3 (AI):
```bash
source venv/bin/activate
python3 generate_with_dalle.py
```

**⏱️ Time**: ~2 minutes for 40 images

### Step 5: Upload to Azure (30 seconds)

```bash
python3 upload_to_azure.py
```

### Step 6: Get Your URLs ✅

Your `image-urls.json` is ready! URLs look like:
```
https://n8ntradingimg.z6.web.core.windows.net/ethereum/ethereum-1.jpg
```

## 🔗 Use in n8n

### Quick Test
1. Open any browser
2. Visit your image URL
3. See your image! 🎉

### Add to n8n Workflow
1. **HTTP Request** node
2. Method: `GET`
3. URL: `https://your-storage.z6.web.core.windows.net/{{$json["asset"]}}/{{$json["asset"]}}-1.jpg`

**Example**:
- Input: `{"asset": "ethereum"}`
- Output: Image of Ethereum trading

## 📱 Test Your Setup

```bash
# Test image access
curl -I https://YOUR-STORAGE.z6.web.core.windows.net/ethereum/ethereum-1.jpg

# Should return: HTTP/1.1 200 OK
```

## 🎯 What You Get

✅ 40 professional trading images
✅ Public URLs for all images
✅ Organized by asset in folders
✅ JSON file for easy n8n integration
✅ Reusable scripts for updates

## 💡 Pro Tips

1. **Bookmark your storage URL**: `https://your-storage.z6.web.core.windows.net/`
2. **Keep `.env` secure**: Never commit to git
3. **Test one asset first**: Comment out others in `config.json`
4. **Use Unsplash for testing**: Free and fast

## 🆘 Common Issues

### Issue: "Module not found"
```bash
source venv/bin/activate  # Activate virtual environment first
pip install -r requirements.txt
```

### Issue: "Azure connection failed"
- Check connection string has no spaces
- Verify static website is enabled
- Wait 2 minutes after enabling

### Issue: "Unsplash rate limit"
- Wait 1 hour (50 requests/hour limit)
- Or get fewer images per run

## ⏭️ Next Steps

1. ✅ Setup complete? → See `README.md` for advanced usage
2. 🔄 Need to update images? → Re-run `fetch_images.py`
3. ➕ Add new assets? → Edit `config.json` + re-run scripts
4. 🔗 n8n integration? → See `README.md` section "n8n Integration"

---

**Total Time**: ~5 minutes | **Cost**: $0 (Unsplash) or ~$2-3 (DALL-E)
