#!/bin/bash

# 1. Create Directories
echo "📂 Creating folder structure..."
mkdir -p src
mkdir -p web
mkdir -p tests
mkdir -p .github/workflows
mkdir -p web/fonts
mkdir -p web/icons

# 2. Setup Python environment
echo "🐍 Setting up Python environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Development Tools Config
echo "⚙️ Configuring development tools..."

# Ruff config
cat <<EOT > pyproject.toml
[tool.ruff]
line-length = 120
select = ["E", "F", "I"]

[tool.ruff.isort]
known-first-party = ["geometry_engine", "svg_renderer", "view_generator", "instrument_geometry"]
EOT

# 4. Verify Backend
echo "🧪 Running backend tests..."
pytest tests/test_instrument_geometry.py

echo "🎉 Project setup and verification complete!"
echo "To start development, run: source venv/bin/activate"
EOT