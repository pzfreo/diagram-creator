from src.logic import generate_plate_svg
import os

print("--- Generating SVG locally ---")
svg_data = generate_plate_svg(length=100, width=50, hole_radius=10)

output_path = "output.svg"
with open(output_path, "w") as f:
    f.write(svg_data)

print(f"✅ Success! Saved to {os.path.abspath(output_path)}")
