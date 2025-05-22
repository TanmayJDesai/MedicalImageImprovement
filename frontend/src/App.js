import React, { useState } from 'react';
import './App.css';

function App() {
  const [image, setImage] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [improvedImage, setImprovedImage] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);

  const [visualHighlights, setVisualHighlights] = useState(false);
  const [descriptions, setDescriptions] = useState(false);

  const apiUrl = 'http://localhost:5002'; // Updated port

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setImage(URL.createObjectURL(file));
      setUploadedFile(file);
      setError('');
      setImprovedImage(null); // Clear previous improved image
    } else {
      setError('Please upload a valid image file.');
    }
  };

  const handleImproveImage = async () => {
    if (!uploadedFile) {
      setError('Please upload an image first.');
      return;
    }

    try {
      setLoading(true);
      setError('');

      // Step 1: Upload the image to the server
      const formData = new FormData();
      formData.append('image', uploadedFile);

      const uploadResponse = await fetch(`${apiUrl}/api/upload`, {
        method: 'POST',
        body: formData,
      });

      const uploadData = await uploadResponse.json();

      if (!uploadResponse.ok) {
        throw new Error(uploadData.error || 'Failed to upload image');
      }

      // Step 2: Request super-resolution processing
      const improveResponse = await fetch(`${apiUrl}/api/improve`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          filename: uploadData.original_image,
        }),
      });

      const improveData = await improveResponse.json();

      if (!improveResponse.ok) {
        throw new Error(improveData.error || 'Failed to improve image');
      }

      // Set the improved image URL
      setImprovedImage(`${apiUrl}/api/images/${improveData.improved_image}`);
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleClearImage = () => {
    setImage(null);
    setUploadedFile(null);
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
        {!image && (
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
        )}
        {image && (
          <div className='toggle-container'>
            <div>
              <span>AI Visual Highlights</span>
              <label className="switch">
                  <input 
                    type="checkbox"
                    checked={visualHighlights}
                    onChange={() => setVisualHighlights(!visualHighlights)}
                  />
                  <span className="slider round"></span>
                </label>
            </div>
            <div>
              <span>AI Descriptions</span>
              <label className="switch">
                <input 
                type="checkbox"
                checked={descriptions}
                onChange={() => setDescriptions(!descriptions)}
                />
                <span className="slider round"></span>
              </label>
            </div>
          </div>
        )}
        
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
          <button 
            className="improve-btn" 
            onClick={handleImproveImage}
            disabled={loading}
          >
            {loading ? 'Processing...' : 'Improve Image'}
          </button>
        )}
        
        {loading && <p className="loading-text">Processing your image. This may take a moment...</p>}
        
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