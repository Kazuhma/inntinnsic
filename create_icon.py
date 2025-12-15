"""
Simple script to create an application icon from emoji
Creates a purple shield icon for Inntinnsic
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a purple shield icon"""
    # Create image with transparency
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Purple color from our theme
    purple = (124, 58, 237, 255)  # #7C3AED

    # Draw shield shape
    # Shield is like an inverted heart shape with pointed bottom
    points = [
        (size * 0.5, size * 0.1),   # Top center
        (size * 0.2, size * 0.15),  # Top left
        (size * 0.15, size * 0.35), # Left side
        (size * 0.2, size * 0.6),   # Lower left
        (size * 0.5, size * 0.9),   # Bottom point
        (size * 0.8, size * 0.6),   # Lower right
        (size * 0.85, size * 0.35), # Right side
        (size * 0.8, size * 0.15),  # Top right
    ]

    draw.polygon(points, fill=purple, outline=purple)

    # Add a lighter inner shield for depth
    lighter_purple = (139, 92, 246, 255)  # Lighter shade
    inner_points = [
        (size * 0.5, size * 0.2),
        (size * 0.3, size * 0.25),
        (size * 0.25, size * 0.4),
        (size * 0.3, size * 0.6),
        (size * 0.5, size * 0.8),
        (size * 0.7, size * 0.6),
        (size * 0.75, size * 0.4),
        (size * 0.7, size * 0.25),
    ]

    draw.polygon(inner_points, fill=lighter_purple, outline=lighter_purple)

    # Save as ICO
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save('icon.ico', format='ICO', sizes=icon_sizes)
    print("Created icon.ico")

    # Also save as PNG for reference
    img.save('icon.png', format='PNG')
    print("Created icon.png")

if __name__ == "__main__":
    create_icon()
