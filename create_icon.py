"""
Simple icon creator for the Mancom Timer application
This creates a basic icon with the Mancom color scheme
"""

def create_simple_icon():
    """Create a simple icon using PIL if available"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create image with Mancom colors
        img = Image.new('RGB', (256, 256), color='#2c3e50')
        draw = ImageDraw.Draw(img)
        
        # Draw a circle for timer
        draw.ellipse((20, 20, 236, 236), outline='#27ae60', width=8)
        
        # Draw timer hand
        center = (128, 128)
        draw.line([(center[0], center[1]), (center[0], 50)], fill='#27ae60', width=6)
        
        # Save icon
        img.save('icon.ico')
        print("✓ Icon created: icon.ico")
        return True
        
    except ImportError:
        print("PIL not installed. Please install with: pip install Pillow")
        print("Or download an icon and save as 'icon.ico'")
        return False

if __name__ == '__main__':
    create_simple_icon()
