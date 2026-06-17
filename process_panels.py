from PIL import Image
import sys

def process(input_path, output_path, col_idx):
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    
    col_w = w // 4
    x0 = col_idx * col_w
    x1 = (col_idx + 1) * col_w
    
    # The bounding box starts a bit from the top, and ends before the text.
    # Text is at the bottom 13% approx.
    # We crop aggressively to remove the borders.
    crop_x0 = x0 + 10
    crop_x1 = x1 - 10
    crop_y0 = int(h * 0.04) + 10 # below the top border
    crop_y1 = int(h * 0.86) - 5  # above the text, maybe above the bottom border
    
    panel = img.crop((crop_x0, crop_y0, crop_x1, crop_y1))
    
    gray = panel.convert("L")
    target_color = (122, 51, 51)
    
    newData = []
    for p, g in zip(panel.getdata(), gray.getdata()):
        orig_alpha = p[3]
        if g > 210:
            alpha = 0
        else:
            alpha = int(((210 - g) / 210.0) * 255.0 * 1.5)
            if alpha > 255: alpha = 255
            elif alpha < 0: alpha = 0
                
        new_alpha = int(alpha * (orig_alpha / 255.0))
        newData.append((target_color[0], target_color[1], target_color[2], new_alpha))
        
    panel.putdata(newData)
    panel.save(output_path, "WEBP", quality=95)

if __name__ == "__main__":
    process(sys.argv[1], "veloura-imgs/sov_celestia_new.webp", 1)
    process(sys.argv[1], "veloura-imgs/sov_promenade_new.webp", 2)
