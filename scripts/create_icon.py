#!/usr/bin/env python3
"""
Create a simple placeholder icon for the application.
"""

from PIL import Image, ImageDraw


def create_icon():
    # Create a 256x256 image
    img = Image.new("RGB", (256, 256), color=(65, 105, 225))  # Royal blue background

    # Draw a simple dashboard-like symbol
    draw = ImageDraw.Draw(img)

    # Draw a rectangle for the dashboard
    draw.rectangle([50, 50, 206, 180], fill=(255, 255, 255), outline=(0, 0, 0), width=2)

    # Draw some grid lines to represent dashboard elements
    for i in range(1, 4):
        y = 50 + i * 35
        draw.line([60, y, 196, y], fill=(200, 200, 200), width=1)

    # Draw some circles as indicators
    for i in range(3):
        for j in range(4):
            x = 70 + j * 35
            y = 70 + i * 40
            draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(65, 105, 225))

    # Save the image
    img.save("src/modular_dashboard/assets/app.iconset/icon_256x256.png")
    print(
        "Created placeholder icon at src/modular_dashboard/assets/app.iconset/icon_256x256.png"
    )


if __name__ == "__main__":
    create_icon()
