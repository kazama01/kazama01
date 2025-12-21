import os
import random
from PIL import Image, ImageDraw, ImageFont

# Config
TEXTS = ["Hello World!", "你好，世界！", "こんにちは世界！", "¡Hola Mundo!", "Bonjour le monde !"]
COLOR = (164, 94, 229)  # #a45ee5
BG_COLOR = (13, 17, 23) # GitHub #0d1117
FONT_SIZE = 40
WIDTH = 435
HEIGHT = 80
# Prioritize fonts with CJK support: Microsoft YaHei, MS Gothic, then fallback
FONT_PATHS = [
    "C:/Windows/Fonts/msyh.ttc",     # Microsoft YaHei (Good for CN/JP)
    "C:/Windows/Fonts/msgothic.ttc", # MS Gothic (Good for JP)
    "C:/Windows/Fonts/courbd.ttf",   # Fallback (No CJK)
    "C:/Windows/Fonts/arial.ttf"
]
OUTPUT_FILE = "glitch_header.gif"

def get_font():
    for font_path in FONT_PATHS:
        if os.path.exists(font_path):
            try:
                # For TTC collections, usually index 0 works
                return ImageFont.truetype(font_path, FONT_SIZE)
            except:
                continue
    return ImageFont.load_default()

def create_base_image(text):
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    font = get_font()
    
    # Center text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (WIDTH - text_w) // 2
    y = (HEIGHT - text_h) // 2
    
    draw.text((x, y), text, font=font, fill=COLOR)
    return img

def glitch_frame(base_img):
    # Convert to numpy-like access
    img = base_img.copy()
    
    # 1. RGB Split (Chromatic Aberration)
    r, g, b = img.split()
    offset_x = random.randint(-4, 4)
    offset_y = random.randint(-4, 4)
    
    r = r.transform(r.size, Image.AFFINE, (1, 0, offset_x, 0, 1, offset_y))
    b = b.transform(b.size, Image.AFFINE, (1, 0, -offset_x, 0, 1, -offset_y))
    
    img = Image.merge("RGB", (r, g, b))
    
    # 2. Slice/Strip Displacement
    # Take horizontal strips and shift them
    for _ in range(random.randint(2, 5)):
        y1 = random.randint(0, HEIGHT - 10)
        h = random.randint(2, 20)
        y2 = min(HEIGHT, y1 + h)
        shift = random.randint(-10, 10)
        
        region = img.crop((0, y1, WIDTH, y2))
        img.paste(region, (shift, y1))
        
    return img

def main():
    frames = []
    
    for text in TEXTS:
        base = create_base_image(text)
        
        # Hold normal text
        for _ in range(10): # 1 second hold
            frames.append(base)
            
        # Glitch transition
        for _ in range(5): # 0.5s glitch
            frames.append(glitch_frame(base))
            
    # Save GIF
    frames[0].save(
        OUTPUT_FILE,
        save_all=True,
        append_images=frames[1:],
        duration=100, # 100ms per frame
        loop=0
    )
    print(f"Glitch GIF saved to {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    main()
