import os
import numpy as np
import cv2
import tensorflow as tf
from tqdm import tqdm

def preprocess_images(input_folder, output_folder, scale_factor=4, img_size=256):
    """
    Preprocess images from the input folder:
    1. Resize to a standard size
    2. Create downscaled versions
    3. Save both original and downscaled versions for training
    
    Args:
        input_folder: Path to the folder containing original X-ray images
        output_folder: Path to save processed images
        scale_factor: Downscaling factor (e.g., 4 means 4x downsampling)
        img_size: Target size for the high-resolution images
    """
    # Create output folders if they don't exist
    os.makedirs(os.path.join(output_folder, 'high_res'), exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'low_res'), exist_ok=True)
    
    # List all files in the input folder
    image_files = [f for f in os.listdir(input_folder) 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff'))]
    
    print(f"Found {len(image_files)} images in {input_folder}")
    
    for img_file in tqdm(image_files, desc="Processing images"):
        # Read image
        img_path = os.path.join(input_folder, img_file)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Read as grayscale for X-rays
        
        if img is None:
            print(f"Warning: Could not read {img_path}")
            continue
        
        # Resize to standard size for high-resolution
        hr_img = cv2.resize(img, (img_size, img_size), interpolation=cv2.INTER_CUBIC)
        
        # Create low-resolution version
        lr_size = img_size // scale_factor
        lr_img = cv2.resize(hr_img, (lr_size, lr_size), interpolation=cv2.INTER_CUBIC)
        
        # Normalize images to [0, 1]
        hr_img = hr_img.astype(np.float32) / 255.0
        lr_img = lr_img.astype(np.float32) / 255.0
        
        # Save processed images
        hr_path = os.path.join(output_folder, 'high_res', img_file)
        lr_path = os.path.join(output_folder, 'low_res', img_file)
        
        # Convert back to uint8 for saving
        cv2.imwrite(hr_path, (hr_img * 255).astype(np.uint8))
        cv2.imwrite(lr_path, (lr_img * 255).astype(np.uint8))
    
    print(f"Processed images saved to {output_folder}")

if __name__ == "__main__":
    # Process images from the NORMAL folder
    preprocess_images("static/NORMAL", "static/processed_data")