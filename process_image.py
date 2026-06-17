from PIL import Image
import sys

def process(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    
    # Remove the top line by cropping the top 8 pixels
    img = img.crop((0, 8, img.width, img.height))
    
    gray = img.convert("L")
    target_color = (122, 51, 51)
    
    newData = []
    for p, g in zip(img.getdata(), gray.getdata()):
        orig_alpha = p[3]
        
        # Hard threshold to ensure light background becomes perfectly transparent
        if g > 210:
            alpha = 0
        else:
            # Map 0 (black stroke) to 255 (opaque), and 210 to 0 (transparent)
            alpha = int(((210 - g) / 210.0) * 255.0 * 1.5)
            if alpha > 255:
                alpha = 255
            elif alpha < 0:
                alpha = 0
                
        new_alpha = int(alpha * (orig_alpha / 255.0))
        newData.append((target_color[0], target_color[1], target_color[2], new_alpha))
        
    img.putdata(newData)
    img.save(output_path, "WEBP", quality=95)

if __name__ == "__main__":
    process(sys.argv[1], sys.argv[2])
