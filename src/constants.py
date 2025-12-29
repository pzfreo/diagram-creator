"""
Constants used across the instrument generator.

This module centralizes all magic numbers and configuration values
to provide a single source of truth and make them easier to maintain.
"""

# Template dimensions (mm)
TEMPLATE_WIDTH_MARGIN = 10.0  # Extra width beyond fingerboard
MIN_FLAT_AREA_HEIGHT = 20.0  # Minimum flat area for text on radius template
ARC_POINT_RESOLUTION = 50  # Number of points to use when rendering arcs

# Text sizing for radius template
TEXT_HEIGHT_FRACTION = 1.0 / 3.0  # Text height as fraction of flat area
TEXT_WIDTH_FACTOR = 0.6  # Approximation factor for text width estimation
TEXT_MARGIN_FRACTION = 0.3  # Margin as fraction of text height

# SVG rendering
SVG_MARGIN = 2.0  # Margin around SVG viewBox (mm)

# Default instrument parameters
DEFAULT_FINGERBOARD_RADIUS = 41.0  # mm, typical for violin
DEFAULT_FB_VISIBLE_HEIGHT_AT_NUT = 3.2  # mm
DEFAULT_FB_VISIBLE_HEIGHT_AT_JOIN = 1.2  # mm
DEFAULT_FB_WIDTH_AT_NUT = 24.0  # mm, typical violin nut width
DEFAULT_FB_WIDTH_AT_END = 42.0  # mm, typical violin end width

# Fret calculation
DEFAULT_FRETS_VIOL = 7
DEFAULT_FRETS_GUITAR = 20
DEFAULT_FRETS_VIOLIN = 0  # No frets

# Numerical precision
EPSILON = 1e-10  # Threshold for detecting parallel lines
