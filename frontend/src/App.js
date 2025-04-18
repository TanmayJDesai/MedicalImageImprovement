import React, { useState } from 'react';
import './App.css';

function App() {
  const [image, setImage] = useState(null);
  const [error, setError] = useState('');
  const [improvedImage, setImprovedImage] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setImage(URL.createObjectURL(file));
      setError('');
    } else {
      setError('Please upload a valid image file.');
    }
  };

  const handleImproveImage = () => {
    if (image) {
      setImprovedImage(image); // Placeholder for improved image logic
    }
  };

  const handleClearImage = () => {
    setImage(null);
    setImprovedImage(null);
  };

  const handleImageClick = (imageUrl) => {
    setSelectedImage(imageUrl);
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>UCLA Medical Image Enhancer</h1>
      </header>
      <main className="App-main">
        <div className="upload-section">
          <input
            type="file"
            accept="image/*"
            className="file-input"
            id="imageUpload"
            onChange={handleFileUpload}
          />
          <label htmlFor="imageUpload" className="upload-btn">
            Upload Image
          </label>
          {error && <p className="error-message">{error}</p>}
        </div>
        
        <div className="image-comparison">
          {image && (
            <div className="image-container">
              <h3>Original Image</h3>
              <div className="image-box" onClick={() => handleImageClick(image)}>
                <img src={image} alt="Original" className="display-image" />
                <button className="clear-btn" onClick={handleClearImage}>
                  X
                </button>
              </div>
            </div>
          )}

          {improvedImage && (
            <div className="image-container">
              <h3>Improved Image</h3>
              <div className="image-box" onClick={() => handleImageClick(improvedImage)}>
                <img src={improvedImage} alt="Improved" className="display-image" />
              </div>
            </div>
          )}
        </div>

        {image && !improvedImage && (
          <button className="improve-btn" onClick={handleImproveImage}>
            Improve Image
          </button>
        )}
        
        {!image && <p className="placeholder-text">Please upload an image to start.</p>}
      </main>

      {/* Modal for viewing images in full screen */}
      {isModalOpen && (
        <div className="modal" onClick={handleModalClose}>
          <div className="modal-content">
            <img
              src={selectedImage}
              alt="Full view"
              className="modal-image"
              onClick={(e) => e.stopPropagation()} // Prevent modal close on image click
            />
            <button className="close-btn" onClick={handleModalClose}>X</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
