#!/bin/bash

# 1. Create Directories
echo "📂 Creating folder structure..."
mkdir -p src
mkdir -p web
mkdir -p tests
mkdir -p .github/workflows

# 2. Create requirements.txt
echo "📝 Creating requirements.txt..."
cat <<EOT >> requirements.txt
build123d
pytest
EOT

# 3. Create .gitignore (Important for git!)
echo "🙈 Creating .gitignore..."
cat <<EOT >> .gitignore
__pycache__/
*.pyc
.DS_Store
venv/
output.svg
EOT

# 4. Create the Core Logic (src/logic.py)
# This is the shared Python code that generates the SVG
echo "🐍 Creating src/logic.py..."
cat <<EOT >> src/logic.py
from build123d import *

def generate_plate_svg(length: float, width: float, hole_radius: float) -> str:
    """
    Generates a 2D plate with a hole and returns the SVG string.
    """
    # Create the Geometry
    with BuildSketch() as sketch:
        Rectangle(length, width)
        Circle(hole_radius, mode=Mode.SUBTRACT)

    # Export to SVG String
    exporter = ExportSVG(scale=1.0)
    exporter.add_shape(sketch.sketch)
    
    return exporter.get_svg_text()
EOT

# 5. Create Local Runner (run_local.py)
# This lets you test on your Mac without a browser
echo "🏃 Creating run_local.py..."
cat <<EOT >> run_local.py
from src.logic import generate_plate_svg
import os

print("--- Generating SVG locally ---")
svg_data = generate_plate_svg(length=100, width=50, hole_radius=10)

output_path = "output.svg"
with open(output_path, "w") as f:
    f.write(svg_data)

print(f"✅ Success! Saved to {os.path.abspath(output_path)}")
EOT

# 6. Create Web Interface (web/index.html)
# A placeholder for the browser interface
echo "🌐 Creating web/index.html..."
cat <<EOT >> web/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Build123d Generator</title>
</head>
<body>
    <h1>Parametric Generator</h1>
    <p>If you see this, the web folder is set up correctly.</p>
</body>
</html>
EOT

# 7. Create Dummy Test (tests/test_logic.py)
echo "🧪 Creating tests/test_logic.py..."
cat <<EOT >> tests/test_logic.py
from src.logic import generate_plate_svg

def test_svg_generation():
    svg = generate_plate_svg(100, 50, 10)
    assert "<svg" in svg
    assert "width" in svg
EOT

echo "🎉 Project setup complete!"
echo "To start, run: python3 -m venv venv && source venv/bin/activate"