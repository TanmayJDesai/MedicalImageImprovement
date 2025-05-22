import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow import keras
from keras import callbacks
from tensorflow.keras import callbacks
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.optimizers import Adam
from model_loader import create_espcn_model
from tqdm import tqdm
import matplotlib.pyplot as plt

def load_dataset(data_dir, batch_size=8, scale_factor=4):
    """
    Create a TensorFlow dataset from processed images.
    
    Args:
        data_dir: Directory containing 'high_res' and 'low_res' subdirectories
        batch_size: Number of image pairs per batch
        scale_factor: Scaling factor between low-res and high-res images
    
    Returns:
        A TensorFlow dataset yielding batches of (lr, hr) pairs
    """
    lr_dir = os.path.join(data_dir, 'low_res')
    hr_dir = os.path.join(data_dir, 'high_res')
    
    lr_images = []
    hr_images = []
    
    image_files = [f for f in os.listdir(hr_dir) 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"Loading {len(image_files)} image pairs...")
    
    for img_file in tqdm(image_files):
        # Load high-res image
        hr_path = os.path.join(hr_dir, img_file)
        hr_img = cv2.imread(hr_path, cv2.IMREAD_GRAYSCALE)
        
        # Load corresponding low-res image
        lr_path = os.path.join(lr_dir, img_file)
        lr_img = cv2.imread(lr_path, cv2.IMREAD_GRAYSCALE)
        
        if hr_img is None or lr_img is None:
            print(f"Warning: Could not load image pair for {img_file}")
            continue
        
        # Normalize to [0, 1]
        hr_img = hr_img.astype(np.float32) / 255.0
        lr_img = lr_img.astype(np.float32) / 255.0
        
        # Add channel dimension for grayscale
        hr_img = np.expand_dims(hr_img, axis=-1)
        lr_img = np.expand_dims(lr_img, axis=-1)
        
        hr_images.append(hr_img)
        lr_images.append(lr_img)
    
    # Convert to numpy arrays
    hr_images = np.array(hr_images)
    lr_images = np.array(lr_images)
    
    # Create TensorFlow Dataset
    dataset = tf.data.Dataset.from_tensor_slices((lr_images, hr_images))
    dataset = dataset.shuffle(buffer_size=len(lr_images))
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    
    return dataset, len(lr_images)

def train_model(data_dir, output_model_path, scale_factor=4, batch_size=8, 
                epochs=100, validation_split=0.2):
    """
    Train an ESPCN super-resolution model.
    
    Args:
        data_dir: Directory containing processed image pairs
        output_model_path: Path to save the trained model
        scale_factor: Upscaling factor
        batch_size: Batch size for training
        epochs: Maximum number of training epochs
        validation_split: Fraction of data to use for validation
    """
    # Create model
    model = create_espcn_model(scale_factor=scale_factor, channels=1)
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='mse',
        metrics=['mae', 'mse']
    )
    
    # Load dataset
    dataset, num_images = load_dataset(data_dir, batch_size, scale_factor)
    
    # Split dataset for validation
    val_size = int(num_images * validation_split)
    train_size = num_images - val_size
    
    train_ds = dataset.take(train_size // batch_size)
    val_ds = dataset.skip(train_size // batch_size)
    
    # Create callbacks
    checkpoint = ModelCheckpoint(
        os.path.join('models', 'espcn_model_epoch_{epoch:02d}.h5'),
        monitor='val_loss',
        save_best_only=True,
        save_weights_only=False,
        mode='min',
        verbose=1
    )
    
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-6,
        verbose=1
    )
    
    # Make sure directories exist
    os.makedirs('models', exist_ok=True)
    
    # Train model
    print(f"Starting training for {epochs} epochs")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[checkpoint, early_stopping, reduce_lr]
    )
    
    # Save final model
    model.save(output_model_path)
    print(f"Model saved to {output_model_path}")
    
    # Plot training history
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss (MSE)')
    plt.legend()
    plt.title('Training and Validation Loss')
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['mae'], label='Train MAE')
    plt.plot(history.history['val_mae'], label='Validation MAE')
    plt.xlabel('Epoch')
    plt.ylabel('Mean Absolute Error')
    plt.legend()
    plt.title('Training and Validation MAE')
    
    plt.tight_layout()
    plt.savefig(os.path.join('models', 'training_history.png'))
    plt.close()

if __name__ == "__main__":
    # Make sure the NORMAL folder has been preprocessed
    if not os.path.exists("static/processed_data"):
        print("Processed data not found. Run preprocess_images.py first.")
    else:
        train_model(
            data_dir="static/processed_data",
            output_model_path="models/espcn_model.h5",
            scale_factor=4,
            batch_size=8,
            epochs=100
        )