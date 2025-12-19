"""
Unit tests for the Build123d logic module.
Run with: python -m pytest tests/test_logic.py -v
"""

import pytest
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from logic import generate_plate_svg, validate_dimensions


class TestValidateDimensions:
    """Tests for the validate_dimensions function"""
    
    def test_valid_dimensions(self):
        """Test with valid dimensions"""
        result = validate_dimensions(100, 50, 10)
        assert result['valid'] is True
        assert len(result['errors']) == 0
    
    def test_negative_length(self):
        """Test rejection of negative length"""
        result = validate_dimensions(-100, 50, 10)
        assert result['valid'] is False
        assert any('Length' in err for err in result['errors'])
    
    def test_zero_width(self):
        """Test rejection of zero width"""
        result = validate_dimensions(100, 0, 10)
        assert result['valid'] is False
        assert any('Width' in err for err in result['errors'])
    
    def test_negative_radius(self):
        """Test rejection of negative radius"""
        result = validate_dimensions(100, 50, -5)
        assert result['valid'] is False
        assert any('radius' in err.lower() for err in result['errors'])
    
    def test_hole_too_large(self):
        """Test rejection when hole is too large for plate"""
        result = validate_dimensions(50, 50, 30)  # 60mm diameter in 50mm plate
        assert result['valid'] is False
        assert any('too large' in err.lower() for err in result['errors'])
    
    def test_excessive_dimensions(self):
        """Test rejection of unreasonably large dimensions"""
        result = validate_dimensions(15000, 50, 10)
        assert result['valid'] is False
        assert any('exceeds maximum' in err.lower() for err in result['errors'])
    
    def test_string_conversion(self):
        """Test that strings are properly converted to floats"""
        result = validate_dimensions("100", "50", "10")
        assert result['valid'] is True
    
    def test_invalid_string(self):
        """Test rejection of non-numeric strings"""
        result = validate_dimensions("abc", "50", "10")
        assert result['valid'] is False
        assert any('valid numbers' in err.lower() for err in result['errors'])
    
    def test_multiple_errors(self):
        """Test that multiple errors are collected"""
        result = validate_dimensions(-100, -50, -10)
        assert result['valid'] is False
        assert len(result['errors']) >= 3


class TestGeneratePlateSVG:
    """Tests for the generate_plate_svg function"""
    
    def test_basic_generation(self):
        """Test basic SVG generation with valid inputs"""
        svg = generate_plate_svg(100, 50, 10)
        
        assert svg is not None
        assert isinstance(svg, str)
        assert len(svg) > 0
        assert svg.strip().startswith('<')
        assert 'svg' in svg.lower()
    
    def test_svg_contains_shapes(self):
        """Test that generated SVG contains expected shape elements"""
        svg = generate_plate_svg(100, 50, 10)
        
        # SVG should contain shape elements
        assert any(tag in svg.lower() for tag in ['path', 'rect', 'circle', 'polygon'])
    
    def test_different_dimensions(self):
        """Test generation with various dimension combinations"""
        test_cases = [
            (50, 50, 5),      # Square plate
            (200, 100, 15),   # Large rectangle
            (30, 20, 3),      # Small plate
            (100.5, 50.25, 10.75)  # Decimal values
        ]
        
        for length, width, radius in test_cases:
            svg = generate_plate_svg(length, width, radius)
            assert svg is not None
            assert len(svg) > 0
    
    def test_negative_length_raises_error(self):
        """Test that negative length raises ValueError"""
        with pytest.raises(ValueError, match="Length must be positive"):
            generate_plate_svg(-100, 50, 10)
    
    def test_zero_width_raises_error(self):
        """Test that zero width raises ValueError"""
        with pytest.raises(ValueError, match="Width must be positive"):
            generate_plate_svg(100, 0, 10)
    
    def test_negative_radius_raises_error(self):
        """Test that negative radius raises ValueError"""
        with pytest.raises(ValueError, match="radius must be positive"):
            generate_plate_svg(100, 50, -5)
    
    def test_hole_too_large_raises_error(self):
        """Test that oversized hole raises ValueError"""
        with pytest.raises(ValueError, match="too large"):
            generate_plate_svg(50, 50, 30)
    
    def test_very_small_dimensions(self):
        """Test with very small but valid dimensions"""
        svg = generate_plate_svg(1, 1, 0.1)
        assert svg is not None
        assert len(svg) > 0
    
    def test_large_dimensions(self):
        """Test with large but valid dimensions"""
        svg = generate_plate_svg(1000, 800, 100)
        assert svg is not None
        assert len(svg) > 0


class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""
    
    def test_hole_at_maximum_size(self):
        """Test hole at maximum allowable size"""
        # For a 100x100 plate, max radius is ~45mm (90% of 50mm half-width)
        svg = generate_plate_svg(100, 100, 22)  # Just under limit
        assert svg is not None
    
    def test_very_thin_plate(self):
        """Test with very thin plate dimensions"""
        svg = generate_plate_svg(200, 5, 1)
        assert svg is not None
    
    def test_square_plate(self):
        """Test with square plate"""
        svg = generate_plate_svg(100, 100, 10)
        assert svg is not None
    
    def test_floating_point_precision(self):
        """Test with high-precision floating point values"""
        svg = generate_plate_svg(100.123456, 50.987654, 10.555555)
        assert svg is not None


@pytest.fixture
def sample_svg():
    """Fixture providing a sample SVG for testing"""
    return generate_plate_svg(100, 50, 10)


class TestSVGStructure:
    """Tests for SVG structure and validity"""
    
    def test_svg_is_valid_xml(self, sample_svg):
        """Test that generated SVG is valid XML"""
        # Basic XML validity checks
        assert sample_svg.count('<svg') == sample_svg.count('</svg>')
        assert '<svg' in sample_svg
        assert sample_svg.strip().endswith('>')
    
    def test_svg_has_viewbox(self, sample_svg):
        """Test that SVG has proper viewBox attribute"""
        # Most CAD-generated SVGs should have viewBox
        # This is a soft check since exact format depends on build123d version
        assert 'viewBox' in sample_svg or 'width' in sample_svg


# Performance and stress tests
class TestPerformance:
    """Performance-related tests"""
    
    @pytest.mark.slow
    def test_generation_speed(self):
        """Test that generation completes in reasonable time"""
        import time
        
        start = time.time()
        generate_plate_svg(100, 50, 10)
        duration = time.time() - start
        
        # Should complete in under 5 seconds
        assert duration < 5.0, f"Generation took {duration:.2f}s"
    
    @pytest.mark.slow
    def test_multiple_generations(self):
        """Test multiple consecutive generations"""
        for i in range(5):
            svg = generate_plate_svg(100 + i*10, 50 + i*5, 10 + i)
            assert svg is not None


if __name__ == '__main__':
    # Allow running tests directly
    pytest.main([__file__, '-v'])
