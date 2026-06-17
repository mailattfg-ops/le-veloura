from PIL import Image
import sys

def process(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    
    gray = img.convert("L")
    target_color = (122, 51, 51)
    
    newData = []
    for p, g in zip(img.getdata(), gray.getdata()):
        orig_alpha = p[3]
        # Very light pixels (white background) become fully transparent
        if g > 230:
            alpha = 0
        else:
            # Darker pixels become the burgundy color with partial transparency for smooth edges
            alpha = int(((230 - g) / 230.0) * 255.0 * 1.5)
            if alpha > 255: alpha = 255
            elif alpha < 0: alpha = 0
                
        new_alpha = int(alpha * (orig_alpha / 255.0))
        newData.append((target_color[0], target_color[1], target_color[2], new_alpha))
        
    img.putdata(newData)
    
    # Crop away the transparent borders to ensure it's tightly framed
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    img.save(output_path, "WEBP", quality=95)

if __name__ == "__main__":
    process(sys.argv[1], sys.argv[2])
