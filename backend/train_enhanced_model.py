import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.optimizers import Adam
from tqdm import tqdm
import matplotlib.pyplot as plt

# Import from your enhanced model loader
from enhanced_model_loader import create_medical_specific_model, create_enhanced_espcn_model

def load_and_preprocess_images(data_dir, target_size=(256, 256)):
    """
    Load and preprocess images with consistent shapes.
    """
    lr_dir = os.path.join(data_dir, 'low_res')
    hr_dir = os.path.join(data_dir, 'high_res')
    
    lr_images = []
    hr_images = []
    
    image_files = [f for f in os.listdir(hr_dir) 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"Loading {len(image_files)} image pairs...")
    
    successful_pairs = 0
    
    for img_file in tqdm(image_files):
        try:
            # Load high-res image
            hr_path = os.path.join(hr_dir, img_file)
            hr_img = cv2.imread(hr_path, cv2.IMREAD_GRAYSCALE)
            
            # Load corresponding low-res image
            lr_path = os.path.join(lr_dir, img_file)
            lr_img = cv2.imread(lr_path, cv2.IMREAD_GRAYSCALE)
            
            if hr_img is None or lr_img is None:
                continue
            
            # Resize to ensure consistent dimensions
            hr_img = cv2.resize(hr_img, target_size, interpolation=cv2.INTER_CUBIC)
            lr_img = cv2.resize(lr_img, (target_size[0]//4, target_size[1]//4), interpolation=cv2.INTER_CUBIC)
            
            # Normalize to [0, 1]
            hr_img = hr_img.astype(np.float32) / 255.0
            lr_img = lr_img.astype(np.float32) / 255.0
            
            # Add channel dimension - this is the key fix!
            hr_img = hr_img[:, :, np.newaxis]  # Shape: (256, 256, 1)
            lr_img = lr_img[:, :, np.newaxis]  # Shape: (64, 64, 1)
            
            hr_images.append(hr_img)
            lr_images.append(lr_img)
            successful_pairs += 1
            
        except Exception as e:
            print(f"Error processing {img_file}: {e}")
            continue
    
    if successful_pairs == 0:
        raise ValueError("No valid image pairs found!")
    
    print(f"Successfully loaded {successful_pairs} image pairs")
    
    # Convert to numpy arrays with consistent shapes
    hr_images = np.stack(hr_images, axis=0)  # Shape: (N, 256, 256, 1)
    lr_images = np.stack(lr_images, axis=0)  # Shape: (N, 64, 64, 1)
    
    print(f"HR images shape: {hr_images.shape}")
    print(f"LR images shape: {lr_images.shape}")
    
    return lr_images, hr_images

def create_dataset(lr_images, hr_images, batch_size=4, validation_split=0.2):
    """
    Create train and validation datasets.
    """
    # Shuffle the data
    indices = np.random.permutation(len(lr_images))
    lr_images = lr_images[indices]
    hr_images = hr_images[indices]
    
    # Split into train and validation
    val_size = int(len(lr_images) * validation_split)
    train_size = len(lr_images) - val_size
    
    lr_train, lr_val = lr_images[:train_size], lr_images[train_size:]
    hr_train, hr_val = hr_images[:train_size], hr_images[train_size:]
    
    print(f"Training samples: {len(lr_train)}")
    print(f"Validation samples: {len(lr_val)}")
    
    # Create TensorFlow datasets
    train_ds = tf.data.Dataset.from_tensor_slices((lr_train, hr_train))
    train_ds = train_ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)
    
    val_ds = tf.data.Dataset.from_tensor_slices((lr_val, hr_val))
    val_ds = val_ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)
    
    return train_ds, val_ds

def train_single_model(model_type, lr_images, hr_images, epochs=50, batch_size=4):
    """
    Train a single model type.
    """
    print(f"\n=== Training {model_type.upper()} Model ===")
    
    try:
        # Create model
        if model_type == "medical":
            model = create_medical_specific_model(scale_factor=4, channels=1)
        elif model_type == "enhanced":
            model = create_enhanced_espcn_model(scale_factor=4, channels=1)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        print(f"Model created with {model.count_params():,} parameters")
        
        # Compile model
        model.compile(
            optimizer=Adam(learning_rate=0.0001),
            loss='mse',
            metrics=['mae']
        )
        
        # Create datasets
        train_ds, val_ds = create_dataset(lr_images, hr_images, batch_size)
        
        # Setup callbacks
        os.makedirs('models', exist_ok=True)
        model_path = f'models/enhanced_{model_type}_model.h5'
        
        callbacks = [
            ModelCheckpoint(
                model_path,
                monitor='val_loss',
                save_best_only=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-6,
                verbose=1
            ),
            EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            )
        ]
        
        # Train model
        print(f"Starting training for {epochs} epochs...")
        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        # Save training plot
        if len(history.history['loss']) > 1:
            plt.figure(figsize=(12, 4))
            
            plt.subplot(1, 2, 1)
            plt.plot(history.history['loss'], label='Train Loss', color='blue')
            plt.plot(history.history['val_loss'], label='Val Loss', color='red')
            plt.xlabel('Epoch')
            plt.ylabel('MSE Loss')
            plt.legend()
            plt.title(f'{model_type.title()} Model - Loss')
            plt.grid(True)
            
            plt.subplot(1, 2, 2)
            plt.plot(history.history['mae'], label='Train MAE', color='blue')
            plt.plot(history.history['val_mae'], label='Val MAE', color='red')
            plt.xlabel('Epoch')
            plt.ylabel('Mean Absolute Error')
            plt.legend()
            plt.title(f'{model_type.title()} Model - MAE')
            plt.grid(True)
            
            plt.tight_layout()
            plot_path = f'models/{model_type}_training_history.png'
            plt.savefig(plot_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"Training plot saved: {plot_path}")
        
        print(f"✅ {model_type.title()} model training completed!")
        print(f"Model saved: {model_path}")
        
        return model_path
        
    except Exception as e:
        print(f"❌ Error training {model_type} model: {e}")
        return None

def main():
    """
    Main training function.
    """
    print("🚀 Starting Enhanced Super-Resolution Training")
    print("=" * 60)
    
    # Check if processed data exists
    data_dir = "static/processed_data"
    if not os.path.exists(data_dir):
        print("❌ ERROR: Processed data not found!")
        print("Please run: python preprocess_images.py")
        return
    
    # Load and preprocess images
    try:
        print("📊 Loading and preprocessing images...")
        lr_images, hr_images = load_and_preprocess_images(data_dir)
    except Exception as e:
        print(f"❌ Error loading images: {e}")
        return
    
    # Train models
    models_to_train = ["medical", "enhanced"]
    successful_models = []
    
    for model_type in models_to_train:
        model_path = train_single_model(
            model_type=model_type,
            lr_images=lr_images,
            hr_images=hr_images,
            epochs=30,  # Reasonable number for testing
            batch_size=2  # Small batch to avoid memory issues
        )
        
        if model_path:
            successful_models.append(model_path)
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 TRAINING SUMMARY")
    print("=" * 60)
    print(f"Successfully trained models: {len(successful_models)}/{len(models_to_train)}")
    
    for i, model_path in enumerate(successful_models, 1):
        print(f"  {i}. {model_path}")
    
    if successful_models:
        print(f"\n🎉 Training completed! You can now run your Flask app.")
        print("Run: python app.py")
    else:
        print("\n😞 No models were successfully trained.")
        print("Please check the error messages above.")

if __name__ == "__main__":
    main()