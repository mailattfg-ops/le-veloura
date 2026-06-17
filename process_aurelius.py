from PIL import Image
import sys

def process(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    
    gray = img.convert("L")
    target_color = (122, 51, 51)
    
    newData = []
    for p, g in zip(img.getdata(), gray.getdata()):
        orig_alpha = p[3]
        
        # More aggressive threshold to completely remove the fake checkerboard background
        # Any pixel lighter than 160 in grayscale will become completely transparent
        if g > 160:
            alpha = 0
        else:
            alpha = int(((160 - g) / 160.0) * 255.0 * 1.5)
            if alpha > 255: alpha = 255
            elif alpha < 0: alpha = 0
                
        new_alpha = int(alpha * (orig_alpha / 255.0))
        newData.append((target_color[0], target_color[1], target_color[2], new_alpha))
        
    img.putdata(newData)
    
    # Crop a few pixels from the edges just in case
    img = img.crop((5, 5, img.width - 5, img.height - 5))
    
    img.save(output_path, "WEBP", quality=95)

if __name__ == "__main__":
    process(sys.argv[1], sys.argv[2])
