from PIL import Image, ImageChops
import glob

def trim_borders(image_path):
    img = Image.open(image_path).convert("RGB")
    
    # We assume the top-left pixel is the background color (usually white)
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    diff = ImageChops.difference(img, bg)
    
    # Convert difference to grayscale and threshold it
    # Any pixel differing from the background by more than 15 will be kept
    diff = diff.convert("L").point(lambda x: 0 if x < 15 else 255)
    bbox = diff.getbbox()
    
    if bbox:
        cropped = img.crop(bbox)
        cropped.save(image_path, "WEBP", quality=90)
        print(f"Cropped {image_path}: {img.size} -> {cropped.size}")
    else:
        print(f"Could not find bounding box for {image_path}")

if __name__ == "__main__":
    files = glob.glob("veloura-imgs/valor_*.webp") + glob.glob("veloura-imgs/vows_*.webp")
    for f in files:
        trim_borders(f)
