import os
import shutil
import random

from pathlib import Path

# Use pathlib for better path handling (cross-platform friendly)
mixed_dir = Path('images/cars')

# Output directories
train_img_dir = Path('dataset/train/images')
train_lbl_dir = Path('dataset/train/labels')
val_img_dir = Path('dataset/val/images')
val_lbl_dir = Path('dataset/val/labels')

# Create output directories if they don't exist
for d in [train_img_dir, train_lbl_dir, val_img_dir, val_lbl_dir]:
    d.mkdir(parents=True, exist_ok=True)

# Get all .jpg files (case-insensitive)
image_files = [f for f in os.listdir(mixed_dir) if f.lower().endswith('.jpg')]
image_files.sort()

# Shuffle and split 80% train, 20% val
random.seed(42)
random.shuffle(image_files)

total = len(image_files)
split_idx = int(0.8 * total)
train_images = image_files[:split_idx]
val_images = image_files[split_idx:]

print(f"📊 Total: {total} | Train: {len(train_images)} | Val: {len(val_images)}")

# Helper function to move image and matching label
def move_files(image_list, img_dst, lbl_dst):
    for img_file in image_list:
        img_src = mixed_dir / img_file
        lbl_file = Path(img_file).stem + '.txt'
        lbl_src = mixed_dir / lbl_file

        shutil.copy2(img_src, img_dst / img_file)

        if lbl_src.exists():
            shutil.copy2(lbl_src, lbl_dst / lbl_file)
        else:
            print(f"⚠️  Missing label for {img_file}, skipping label copy.")

# Move files
move_files(train_images, train_img_dir, train_lbl_dir)
move_files(val_images, val_img_dir, val_lbl_dir)

print("✅ Dataset split complete: Check 'dataset/train' and 'dataset/val'.")
