#!/bin/bash
# =============================================================================
# n8n Trading Images - Setup Script
# =============================================================================

set -e

echo "=================================================="
echo "🚀 n8n Trading Images Setup"
echo "=================================================="

# Check Python version
echo ""
echo "📋 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION detected"

# Create virtual environment
echo ""
echo "🔨 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Create .env file if it doesn't exist
echo ""
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your API keys!"
    echo "   - For Unsplash: Add UNSPLASH_ACCESS_KEY"
    echo "   - For DALL-E: Add AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY"
    echo "   - For Azure Storage: Add AZURE_STORAGE_CONNECTION_STRING"
else
    echo "✓ .env file already exists"
fi

# Make scripts executable
echo ""
echo "🔐 Making scripts executable..."
chmod +x fetch_images.py
chmod +x generate_with_dalle.py
chmod +x upload_to_azure.py
echo "✅ Scripts are executable"

# Summary
echo ""
echo "=================================================="
echo "✨ Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Choose your image source:"
echo "   • Option A (Free): python3 fetch_images.py"
echo "   • Option B (AI):   python3 generate_with_dalle.py"
echo "3. Upload to Azure: python3 upload_to_azure.py"
echo ""
echo "For detailed instructions, see README.md"
echo ""
