import os

def create_directory_structure():
    """Create the necessary directory structure for the project."""
    directories = [
        "static",
        "static/NORMAL",
        "static/processed_data",
        "static/processed_data/high_res",
        "static/processed_data/low_res",
        "uploads",
        "uploads/improved",
        "models",
        "templates"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    print("\nDirectory structure created successfully!")
    print("\nNext steps:")
    print("1. Place your chest X-ray images in the 'static/NORMAL' directory")
    print("2. Run 'python preprocess_images.py' to prepare the training data")
    print("3. Run 'python train_model.py' to train the super-resolution model")
    print("4. Run 'python app.py' to start the Flask server")

if __name__ == "__main__":
    create_directory_structure()