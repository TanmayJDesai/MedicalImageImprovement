import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, UpSampling2D
from tensorflow.keras.optimizers import Adam

# Load and blur the images
def blur_images(image_paths):
    blurred_images = []
    for path in image_paths:
        image = cv2.imread(path)
        blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
        blurred_images.append(blurred_image)
    return np.array(blurred_images)

# Load the dataset
image_paths = ['image1.jpg', 'image2.jpg', 'image3.jpg']
blurred_images = blur_images(image_paths)

# Define the ESPCN model
model = Sequential()
model.add(Conv2D(64, (5, 5), activation='relu', padding='same', input_shape=(None, None, 3)))
model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(3, (3, 3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

# Train the model
model.fit(blurred_images, blurred_images, batch_size=16, epochs=10)

# Save the trained model
model.save('espcn_model.h5')
