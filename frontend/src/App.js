import React, { useState } from 'react';
import './App.css';

function App() {
  const [originalImage, setOriginalImage] = useState(null);
  const [improvedImage, setImprovedImage] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setOriginalImage(URL.createObjectURL(file));
      setImprovedImage(null);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select an image first.');
      return;
    }

    setIsUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        body: formData
      });
      
      const data = await response.json();

      if (data.success) {
        // Store the filename for improvement request
        setSelectedFile({ ...selectedFile, serverFilename: data.original_image });
      } else {
        setError('Upload failed.');
      }
    } catch (error) {
      console.error('Error uploading image:', error);
      setError('Error uploading image. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleImprove = async () => {
    if (!selectedFile || !selectedFile.serverFilename) {
      setError('Please upload an image first.');
      return;
    }

    setIsProcessing(true);
    setError('');

    try {
      const response = await fetch('http://localhost:5000/api/improve', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          filename: selectedFile.serverFilename
        })
      });
      
      const data = await response.json();

      if (data.success) {
        const improvedImageUrl = `http://localhost:5000/api/images/${data.improved_image}?t=${new Date().getTime()}`;
        setImprovedImage(improvedImageUrl);
      } else {
        setError('Image improvement failed.');
      }
    } catch (error) {
      console.error('Error improving image:', error);
      setError('Error improving image. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleClear = () => {
    setOriginalImage(null);
    setImprovedImage(null);
    setSelectedFile(null);
    // Reset the file input
    const fileInput = document.getElementById('image-upload');
    if (fileInput) fileInput.value = '';
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Image Improvement Tool</h1>
      </header>
      
      <main className="App-main">
        <div className="upload-section">
          <input 
            type="file" 
            id="image-upload" 
            accept="image/*" 
            onChange={handleFileChange} 
            className="file-input"
          />
          <label htmlFor="image-upload" className="upload-btn">
            Select Image
          </label>
          
          <button 
            onClick={handleUpload} 
            disabled={!selectedFile || isUploading}
            className="upload-btn"
          >
            {isUploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="image-comparison">
          <div className="image-container">
            <h2>Original Image</h2>
            <div className="image-box">
              {originalImage ? (
                <>
                  <button className="clear-btn" onClick={handleClear}>✕</button>
                  <img src={originalImage} alt="Original" className="display-image" />
                </>
              ) : (
                <p className="placeholder-text">No image selected</p>
              )}
            </div>
          </div>
          
          <div className="improve-section">
            <button 
              onClick={handleImprove} 
              disabled={!selectedFile || !selectedFile.serverFilename || isProcessing}
              className="improve-btn"
            >
              {isProcessing ? 'Processing...' : 'Improve'}
            </button>
          </div>
          
          <div className="image-container">
            <h2>Improved Image</h2>
            <div className="image-box">
              {improvedImage ? (
                <img src={improvedImage} alt="Improved" className="display-image" />
              ) : (
                <p className="placeholder-text">Improved image will appear here</p>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;