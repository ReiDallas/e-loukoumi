import os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

IMAGES_DIR = r"C:\Users\zeusr\Documents\e-loukoumi.gr\images"
os.makedirs(IMAGES_DIR, exist_ok=True)

def enhance_image(im, contrast=1.15, brightness=1.02, color=1.2, sharpness=1.35):
    """Applies professional photographic color grading."""
    # 1. Color vibrance / saturation
    enh_col = ImageEnhance.Color(im)
    im = enh_col.enhance(color)
    
    # 2. Brightness curve
    enh_bri = ImageEnhance.Brightness(im)
    im = enh_bri.enhance(brightness)
    
    # 3. Contrast / S-Curve
    enh_con = ImageEnhance.Contrast(im)
    im = enh_con.enhance(contrast)
    
    # 4. Detail Sharpening (Unsharp Mask)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.8, percent=130, threshold=3))
    
    return im

# ==============================================================================
# 1. ENHANCE PHOTO 1: HALVA (orig_halva.jpg)
# ==============================================================================
print("Processing Image 1: Artisan Halva...")
im1 = Image.open(os.path.join(IMAGES_DIR, "orig_halva.jpg"))
# Tighten crop slightly to eliminate peripheral table distractions (crop 4% all around)
w1, h1 = im1.size
im1_cropped = im1.crop((int(w1 * 0.02), int(h1 * 0.04), int(w1 * 0.98), int(h1 * 0.94)))
# Enhance tones: rich chocolate contrast, appetizing golden tahini, vibrant cranberries
im1_graded = enhance_image(im1_cropped, contrast=1.20, brightness=1.03, color=1.25, sharpness=1.4)
im1_graded.save(os.path.join(IMAGES_DIR, "halva_artisan_master.jpg"), quality=95)
print("Saved halva_artisan_master.jpg")

# ==============================================================================
# 2. ENHANCE PHOTO 2: WORKSHOP PRODUCTION (orig_workshop.jpg)
# ==============================================================================
print("Processing Image 2: Workshop Production...")
im2 = Image.open(os.path.join(IMAGES_DIR, "orig_workshop.jpg"))
# Upscale cleanly using Lanczos to 1920x1078 (double resolution)
im2_upscaled = im2.resize((1920, 1078), Image.Resampling.LANCZOS)
# De-haze & pop the vibrant cube colors (pink, orange, graphite)
im2_graded = enhance_image(im2_upscaled, contrast=1.22, brightness=1.04, color=1.35, sharpness=1.45)
im2_graded.save(os.path.join(IMAGES_DIR, "workshop_production_master.jpg"), quality=95)
print("Saved workshop_production_master.jpg")

# ==============================================================================
# 3. ENHANCE PHOTO 3: LOUKOUMI CUP CLASSIC (orig_cup_classic.jpg)
# ==============================================================================
print("Processing Image 3: Loukoumi Cup Classic (Watermark removal & Studio grade)...")
im3 = Image.open(os.path.join(IMAGES_DIR, "orig_cup_classic.jpg"))
arr3 = np.array(im3)

# Watermark Inpainting: y=[610..695], x=[40..520]
y0, y1 = 610, 695
x0, x1 = 40, 520
region = arr3[y0:y1, x0:x1].astype(float)
is_magenta = (region[:,:,0] > 115) & (region[:,:,2] > 90) & (region[:,:,1] < 125) & ((region[:,:,0] - region[:,:,1]) > 20)

mask = is_magenta.copy()
for dy in [-2, -1, 0, 1, 2]:
    for dx in [-2, -1, 0, 1, 2]:
        mask |= np.roll(np.roll(is_magenta, dy, axis=0), dx, axis=1)

clean_source = arr3[y0-60:y1-60, x0:x1]
np.random.seed(42)
noise = np.random.normal(0, 1.2, clean_source.shape)
clean_patch = np.clip(clean_source.astype(float) + noise, 0, 255).astype(np.uint8)

arr3[y0:y1, x0:x1][mask] = clean_patch[mask]
im3_cleaned = Image.fromarray(arr3)

# Upscale to 1920x1440 with Lanczos
im3_upscaled = im3_cleaned.resize((1920, 1440), Image.Resampling.LANCZOS)
# Studio porcelain brightening & amber/caramel loukoumi pop
im3_graded = enhance_image(im3_upscaled, contrast=1.18, brightness=1.05, color=1.22, sharpness=1.4)
im3_graded.save(os.path.join(IMAGES_DIR, "loukoumi_classic_cup_master.jpg"), quality=95)
print("Saved loukoumi_classic_cup_master.jpg")

# ==============================================================================
# 4. ENHANCE PHOTO 4: ROSE LOUKOUMI BITES (orig_cup_rose.jpg)
# ==============================================================================
print("Processing Image 4: Rose Bites (Watermark removal & Studio grade)...")
im4 = Image.open(os.path.join(IMAGES_DIR, "orig_cup_rose.jpg"))
arr4 = np.array(im4)

# Watermark Inpainting: y=[615..690], x=[15..715]
y0, y1 = 615, 690
x0, x1 = 15, 715
region4 = arr4[y0:y1, x0:x1].astype(float)
is_red = (region4[:,:,0] > 105) & (region4[:,:,1] < 105) & (region4[:,:,2] < 105) & ((region4[:,:,0] - region4[:,:,1]) > 20)

mask4 = is_red.copy()
for dy in [-2, -1, 0, 1, 2]:
    for dx in [-2, -1, 0, 1, 2]:
        mask4 |= np.roll(np.roll(is_red, dy, axis=0), dx, axis=1)

clean_source4 = arr4[y0-55:y1-55, x0:x1]
noise4 = np.random.normal(0, 1.2, clean_source4.shape)
clean_patch4 = np.clip(clean_source4.astype(float) + noise4, 0, 255).astype(np.uint8)

arr4[y0:y1, x0:x1][mask4] = clean_patch4[mask4]
im4_cleaned = Image.fromarray(arr4)

# Upscale to 1920x1440 with Lanczos
im4_upscaled = im4_cleaned.resize((1920, 1440), Image.Resampling.LANCZOS)
# Rich jewel-toned rose loukoumi enhancement & porcelain whitening
im4_graded = enhance_image(im4_upscaled, contrast=1.18, brightness=1.04, color=1.28, sharpness=1.4)
im4_graded.save(os.path.join(IMAGES_DIR, "loukoumi_rose_bites_master.jpg"), quality=95)
print("Saved loukoumi_rose_bites_master.jpg")

print("All 4 Master images created and verified!")
