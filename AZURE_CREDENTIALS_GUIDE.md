# 🔑 Azure Credentials Guide

## What You Need to Provide

Based on your existing Azure setup, here's what credentials I need to complete the image library:

---

## 🎯 Required Credentials

### 1. Azure Storage Account (Required for Both Options)

**Purpose**: Store and serve images with public URLs for n8n

**What I Need**:
```bash
# Option 1: Connection String (Recommended)
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=xxx;AccountKey=xxx;EndpointSuffix=core.windows.net

# Option 2: Account Name + Key
AZURE_STORAGE_ACCOUNT_NAME=your-storage-account
AZURE_STORAGE_ACCOUNT_KEY=your-key
```

**Where to Get It**:
1. Azure Portal → **Storage Accounts**
2. Select/Create storage account
3. Go to **Security + networking** → **Access keys**
4. Show and copy **Connection string** from Key1

**Or Create New**:
```bash
# You can create via Azure Portal:
- Name: n8ntradingimg (or any unique name)
- Resource Group: AZAI_group
- Region: Sweden Central (same as your Logic App)
- Performance: Standard
- Redundancy: LRS (cheapest)
- Cost: ~$0.02/GB/month (~$0.002 for 40 images)
```

---

## 🎨 Image Source Options

### Option A: Unsplash API (FREE - Recommended)

**Purpose**: Fetch professional stock photos for free

**What I Need**:
```bash
UNSPLASH_ACCESS_KEY=your_access_key_here
```

**Where to Get It**:
1. Go to [unsplash.com/developers](https://unsplash.com/developers)
2. Sign up/Log in
3. Click **New Application**
4. Accept terms
5. Copy **Access Key**

**Details**:
- ✅ **Cost**: FREE
- ✅ **Rate Limit**: 50 requests/hour (enough for 40 images)
- ✅ **Quality**: Professional photography
- ✅ **Setup Time**: 2 minutes

---

### Option B: Azure OpenAI DALL-E 3 (AI-Generated)

**Purpose**: Generate custom AI images with specific prompts

**What I Need**:
```bash
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_DALLE_DEPLOYMENT=dall-e-3
```

**Your Existing Resource**: `https://brn-azai.openai.azure.com/`

**Where to Get Credentials**:
1. Azure Portal → **Azure OpenAI** → **brn-azai**
2. Go to **Resource Management** → **Keys and Endpoint**
3. Copy:
   - **Endpoint**: `https://brn-azai.openai.azure.com/`
   - **Key 1**: Your API key

**Check DALL-E 3 Deployment**:
1. Go to [Azure OpenAI Studio](https://oai.azure.com/)
2. Select your resource: **brn-azai**
3. Click **Deployments**
4. Look for `dall-e-3` deployment

**If DALL-E 3 Not Deployed**:
1. Azure OpenAI Studio → **Deployments** → **Create new deployment**
2. Select model: **dall-e-3**
3. Deployment name: **dall-e-3**
4. **Deploy**
5. Wait 5-10 minutes

**Details**:
- 💰 **Cost**: ~$0.04 per image (standard) or $0.08 (HD)
- 💰 **Total**: $1.60 - $3.20 for 40 images (one-time)
- ✅ **Quality**: Custom AI-generated, consistent style
- ✅ **Setup Time**: 5 minutes (if DALL-E already deployed)

---

## 🎯 My Recommendation

### For Quick Testing & Production
**Use Unsplash** (Option A):
- Free forever
- Professional quality
- No Azure OpenAI costs
- 2-minute setup
- Perfect for n8n automation

### For Custom Brand Style
**Use DALL-E 3** (Option B):
- Custom-generated images
- Consistent visual style
- Full control over image content
- ~$2-3 one-time cost
- Use existing Azure OpenAI resource

---

## 📋 What To Do Next

### Choose Your Path:

#### 🆓 Path A: Free Images (Unsplash)
1. ✅ Create Unsplash account → Get API key
2. ✅ Create Azure Storage Account → Get connection string
3. ✅ Run: `./setup.sh`
4. ✅ Edit `.env` with credentials
5. ✅ Run: `python3 fetch_images.py`
6. ✅ Run: `python3 upload_to_azure.py`

**Provide**:
```bash
UNSPLASH_ACCESS_KEY=xxx
AZURE_STORAGE_CONNECTION_STRING=xxx
```

#### 🤖 Path B: AI Images (DALL-E 3)
1. ✅ Get Azure OpenAI credentials (you already have this)
2. ✅ Verify DALL-E 3 deployment exists
3. ✅ Create Azure Storage Account → Get connection string
4. ✅ Run: `./setup.sh`
5. ✅ Edit `.env` with credentials
6. ✅ Run: `python3 generate_with_dalle.py`
7. ✅ Run: `python3 upload_to_azure.py`

**Provide**:
```bash
AZURE_OPENAI_ENDPOINT=https://brn-azai.openai.azure.com/
AZURE_OPENAI_API_KEY=xxx
AZURE_STORAGE_CONNECTION_STRING=xxx
```

---

## 🔐 Security Notes

1. **Never commit `.env` to git** - it contains secrets
2. **Keep connection strings private** - they grant full storage access
3. **Rotate keys regularly** - especially if exposed
4. **Use managed identities in production** - for enhanced security

---

## ❓ Need Help?

**Which credentials to provide?**

Tell me:
1. Do you want **FREE images (Unsplash)** or **AI-generated (DALL-E)**?
2. Do you already have a **Storage Account** or should I guide you to create one?

Then provide the relevant credentials above.

---

## 📊 Summary Table

| Credential | Required For | Cost | How to Get |
|------------|-------------|------|------------|
| **Azure Storage Connection String** | Both options | ~$0.002/month | Azure Portal → Storage → Access Keys |
| **Unsplash API Key** | Option A only | FREE | unsplash.com/developers |
| **Azure OpenAI Endpoint + Key** | Option B only | ~$2-3 one-time | Azure Portal → OpenAI → Keys |

---

**Ready?** Just tell me which option you prefer and provide the credentials! 🚀
