from build123d import *
import os

def generate_plate_svg(length: float, width: float, hole_radius: float) -> str:
    """
    Generates a 2D plate with a hole and returns the SVG string.
    """
    # 1. Create the Geometry
    with BuildSketch() as builder:
        Rectangle(length, width)
        Circle(hole_radius, mode=Mode.SUBTRACT)

    # 2. Export to SVG String
    temp_filename = "temp_export.svg"
    
    exporter = ExportSVG(scale=1.0)
    
    # CRITICAL FIX: We must pass 'builder.sketch', which is the actual shape.
    # Passing just 'builder' causes the "not iterable" error.
    exporter.add_shape(builder.sketch)
    
    exporter.write(temp_filename)

    # 3. Read the file content into a string
    with open(temp_filename, "r") as f:
        svg_text = f.read()

    # 4. Cleanup
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
        
    return svg_text