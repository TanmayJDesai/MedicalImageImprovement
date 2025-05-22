import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
import numpy as np
import os
import cv2

def create_enhanced_espcn_model(scale_factor=4, channels=1):
    """
    Create an enhanced ESPCN model with better architecture for super-resolution.
    
    Args:
        scale_factor: Upscaling factor (e.g., 4 for 4x upscaling)
        channels: Number of channels in the input image (1 for grayscale)
    
    Returns:
        A Keras model for super-resolution
    """
    inputs = layers.Input(shape=(None, None, channels))
    
    # Enhanced feature extraction with residual connections
    x = layers.Conv2D(128, kernel_size=9, padding="same", activation="relu")(inputs)
    
    # Residual blocks for better feature learning
    for i in range(6):
        residual = x
        x = layers.Conv2D(128, kernel_size=3, padding="same", activation="relu")(x)
        x = layers.Conv2D(128, kernel_size=3, padding="same")(x)
        x = layers.Add()([x, residual])  # Residual connection
        x = layers.Activation("relu")(x)
    
    # Additional feature extraction
    x = layers.Conv2D(64, kernel_size=3, padding="same", activation="relu")(x)
    x = layers.Conv2D(32, kernel_size=3, padding="same", activation="relu")(x)
    
    # Sub-pixel convolution (pixel shuffling)
    x = layers.Conv2D(
        channels * (scale_factor ** 2), kernel_size=3, padding="same"
    )(x)
    outputs = tf.nn.depth_to_space(x, scale_factor)
    
    return models.Model(inputs, outputs)

def create_srgan_generator(scale_factor=4, channels=1):
    """
    Create a SRGAN-style generator for even better super-resolution.
    """
    inputs = layers.Input(shape=(None, None, channels))
    
    # Initial convolution
    x = layers.Conv2D(64, kernel_size=9, padding="same")(inputs)
    x = layers.PReLU()(x)
    skip_connection = x
    
    # Residual blocks with batch normalization
    for i in range(16):
        residual = x
        x = layers.Conv2D(64, kernel_size=3, padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.PReLU()(x)
        x = layers.Conv2D(64, kernel_size=3, padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.Add()([x, residual])
    
    # Post-residual block
    x = layers.Conv2D(64, kernel_size=3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Add()([x, skip_connection])
    
    # Upsampling blocks
    for i in range(int(np.log2(scale_factor))):
        x = layers.Conv2D(256, kernel_size=3, padding="same")(x)
        x = tf.nn.depth_to_space(x, 2)
        x = layers.PReLU()(x)
    
    # Final output
    outputs = layers.Conv2D(channels, kernel_size=9, padding="same", activation="tanh")(x)
    
    return models.Model(inputs, outputs)

def create_medical_specific_model(scale_factor=4, channels=1):
    """
    Create a model specifically optimized for medical X-ray images.
    """
    inputs = layers.Input(shape=(None, None, channels))
    
    # Initial feature extraction with larger receptive field
    x = layers.Conv2D(64, kernel_size=7, padding="same", activation="relu")(inputs)
    
    # Multi-scale feature extraction
    # Branch 1: Small details
    branch1 = layers.Conv2D(32, kernel_size=3, padding="same", activation="relu")(x)
    branch1 = layers.Conv2D(32, kernel_size=3, padding="same", activation="relu")(branch1)
    
    # Branch 2: Medium details
    branch2 = layers.Conv2D(32, kernel_size=5, padding="same", activation="relu")(x)
    branch2 = layers.Conv2D(32, kernel_size=5, padding="same", activation="relu")(branch2)
    
    # Branch 3: Large details
    branch3 = layers.Conv2D(32, kernel_size=7, padding="same", activation="relu")(x)
    branch3 = layers.Conv2D(32, kernel_size=7, padding="same", activation="relu")(branch3)
    
    # Combine multi-scale features
    x = layers.Concatenate()([branch1, branch2, branch3])
    
    # Dense residual blocks
    for i in range(8):
        residual = x
        x = layers.Conv2D(96, kernel_size=3, padding="same", activation="relu")(x)
        x = layers.Conv2D(96, kernel_size=3, padding="same")(x)
        x = layers.Add()([x, residual])
        x = layers.Activation("relu")(x)
    
    # Final feature processing
    x = layers.Conv2D(64, kernel_size=3, padding="same", activation="relu")(x)
    
    # Sub-pixel convolution
    x = layers.Conv2D(
        channels * (scale_factor ** 2), kernel_size=3, padding="same"
    )(x)
    outputs = tf.nn.depth_to_space(x, scale_factor)
    
    return models.Model(inputs, outputs)

def load_model(model_path, model_type="enhanced"):
    """
    Load a trained super-resolution model.
    
    Args:
        model_path: Path to the saved model
        model_type: Type of model to create if none exists
    
    Returns:
        A loaded Keras model
    """
    if os.path.exists(model_path):
        return tf.keras.models.load_model(model_path)
    else:
        print(f"Model not found at {model_path}. Creating a new {model_type} model.")
        if model_type == "enhanced":
            return create_enhanced_espcn_model()
        elif model_type == "srgan":
            return create_srgan_generator()
        elif model_type == "medical":
            return create_medical_specific_model()
        else:
            return create_enhanced_espcn_model()

def advanced_preprocess_image(img_path):
    """
    Advanced preprocessing for better results.
    """
    # Read image
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not read image: {img_path}")
    
    # Histogram equalization for better contrast
    img = cv2.equalizeHist(img)
    
    # Gaussian blur to reduce noise
    img = cv2.GaussianBlur(img, (3, 3), 0.5)
    
    # Normalize
    img = img.astype(np.float32) / 255.0
    
    # Ensure divisible by scale factor
    h, w = img.shape
    new_h = (h // 4) * 4
    new_w = (w // 4) * 4
    img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    
    return img

def process_image_advanced(img_path, model, scale_factor=4):
    """
    Process an image through the super-resolution model with advanced techniques.
    """
    # Advanced preprocessing
    lr_img = advanced_preprocess_image(img_path)
    
    # Prepare for model input
    lr_img = np.expand_dims(lr_img, axis=-1)  # Add channel dimension
    lr_img = np.expand_dims(lr_img, axis=0)   # Add batch dimension
    
    # Generate super-resolution image
    sr_img = model.predict(lr_img)
    
    # Post-process
    sr_img = np.squeeze(sr_img)  # Remove batch and channel dimensions
    sr_img = np.clip(sr_img, 0, 1)
    
    # Apply sharpening filter
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sr_img_uint8 = (sr_img * 255).astype(np.uint8)
    sharpened = cv2.filter2D(sr_img_uint8, -1, kernel)
    
    # Blend original and sharpened (80% sharpened, 20% original)
    final_img = cv2.addWeighted(sharpened, 0.8, sr_img_uint8, 0.2, 0)
    
    # Additional contrast enhancement
    final_img = cv2.equalizeHist(final_img)
    
    return sr_img_uint8, final_img