import fitz
import io
from PIL import Image
import sys

def extract_images(pdf_path, prefix, output_dir):
    doc = fitz.open(pdf_path)
    count = 1
    extracted = []
    for i in range(len(doc)):
        page = doc[i]
        # Render the page to a pixmap
        pix = page.get_pixmap(dpi=200)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        filename = f"{output_dir}/{prefix}_{count:02d}.webp"
        img.save(filename, "WEBP", quality=90)
        extracted.append(filename)
        count += 1
    return extracted

if __name__ == "__main__":
    groom_pdf = r"C:\Users\HP\Downloads\GROOM.pdf"
    bride_pdf = r"C:\Users\HP\Downloads\BRIDE.pdf"
    
    try:
        groom_imgs = extract_images(groom_pdf, "valor", "veloura-imgs")
        print("GROOM:", groom_imgs)
    except Exception as e:
        print("Error processing GROOM:", e)
        
    try:
        bride_imgs = extract_images(bride_pdf, "vows", "veloura-imgs")
        print("BRIDE:", bride_imgs)
    except Exception as e:
        print("Error processing BRIDE:", e)
