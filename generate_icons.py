"""
Generate PWA icon files from SVG source.
This script creates the required PNG icons for the PWA.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
import numpy as np


def create_icon(size, filename):
    """Create an icon of specified size."""
    # Create figure with exact pixel dimensions
    dpi = 100
    fig_size = size / dpi
    fig = plt.figure(figsize=(fig_size, fig_size), dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim(0, 512)
    ax.set_ylim(0, 512)
    ax.axis('off')

    # Background with rounded corners
    background = FancyBboxPatch(
        (0, 0), 512, 512,
        boxstyle="round,pad=0,rounding_size=64",
        facecolor='#4F46E5',
        edgecolor='none'
    )
    ax.add_patch(background)

    # Instrument neck body (simplified violin shape)
    # Define the neck outline
    neck_x = [196, 206, 215, 225, 227, 225, 215, 206, 196, 286, 296, 306, 315, 317, 315, 306, 296, 286]
    neck_y = [76, 156, 196, 276, 356, 436, 476, 516, 516, 516, 476, 436, 356, 276, 196, 156, 76, 76]

    ax.fill(neck_x, neck_y, color='white', alpha=0.95, zorder=2)

    # Fingerboard (darker center strip)
    fingerboard = Rectangle(
        (226, 76), 60, 440,
        facecolor='#2D2A6E',
        alpha=0.8,
        zorder=3
    )
    ax.add_patch(fingerboard)

    # Fret markers (dots)
    fret_positions = [136, 196, 256, 316, 376]
    for y in fret_positions:
        circle = Circle((256, y), 6, color='white', alpha=0.7, zorder=4)
        ax.add_patch(circle)

    # Strings
    string_positions = [241, 251, 261, 271]
    for x in string_positions:
        ax.plot([x, x], [66, 526], color='white', linewidth=1.5, alpha=0.4, zorder=4)

    # Save with exact dimensions
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    plt.savefig(
        filename,
        dpi=dpi,
        bbox_inches='tight',
        pad_inches=0,
        facecolor='none',
        transparent=False
    )
    plt.close(fig)
    print(f"✓ Created {filename} ({size}x{size})")


def main():
    """Generate all required icon sizes."""
    print("Generating PWA icons...")

    # Create icon directory if it doesn't exist
    import os
    os.makedirs('web/icons', exist_ok=True)

    # Generate required sizes
    create_icon(192, 'web/icons/icon-192x192.png')
    create_icon(512, 'web/icons/icon-512x512.png')

    print("\n✓ All icons generated successfully!")
    print("\nNote: favicon.ico should be created from icon-192x192.png")
    print("You can use online tools like https://convertio.co/png-ico/ or")
    print("ImageMagick: convert web/icons/icon-192x192.png -define icon:auto-resize=64,48,32,16 web/favicon.ico")


if __name__ == '__main__':
    main()
