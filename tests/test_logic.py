from src.logic import generate_plate_svg

def test_svg_generation():
    svg = generate_plate_svg(100, 50, 10)
    assert "<svg" in svg
    assert "width" in svg
