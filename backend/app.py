import os
import uuid
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS
from enhanced_model_loader import load_model, process_image_advanced

app = Flask(__name__, static_folder='static')

# Configure CORS properly
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"], 
     methods=["GET", "POST", "OPTIONS"], 
     allow_headers=["Content-Type", "Authorization"])

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'improved'), exist_ok=True)

# Load the enhanced super-resolution model
MODEL_PATH = 'models/espcn_model_enhanced_medical.h5'  # Use the best performing model
model = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def load_sr_model():
    global model
    if model is None:
        try:
            model = load_model(MODEL_PATH)
            print("Super-resolution model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Continuing without model - will use fallback image copying")
            model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    # Handle preflight requests
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    print("Upload request received")
    
    if 'image' not in request.files:
        print("No image in request")
        return jsonify({'error': 'No image part'}), 400
    
    file = request.files['image']
    print(f"File received: {file.filename}")
    
    if file.filename == '':
        print("No filename")
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        filename_parts = os.path.splitext(original_filename)
        unique_filename = f"{filename_parts[0]}_{str(uuid.uuid4())}{filename_parts[1]}"
        
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(original_path)
        print(f"File saved as: {unique_filename}")
        
        response = jsonify({
            'success': True,
            'original_image': unique_filename
        })
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        return response
    
    print("File type not allowed")
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/api/improve', methods=['POST', 'OPTIONS'])
def improve_image():
    # Handle preflight requests
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    load_sr_model()
    
    print("Improve request received")
    data = request.json
    print(f"Request data: {data}")
    
    if not data or 'filename' not in data:
        return jsonify({'error': 'No filename provided'}), 400
    
    original_filename = data['filename']
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    print(f"Looking for file: {original_path}")
    
    if not os.path.exists(original_path):
        print(f"File not found: {original_path}")
        return jsonify({'error': 'Original image not found'}), 404
    
    if model is None:
        print("Model not available, using fallback copy method")
        # Fall back to a simple copy if model isn't available
        improved_filename = f"improved_{original_filename}"
        improved_path = os.path.join(app.config['UPLOAD_FOLDER'], 'improved', improved_filename)
        import shutil
        shutil.copy(original_path, improved_path)
        
        response = jsonify({
            'success': True,
            'original_image': original_filename,
            'improved_image': f"improved/{improved_filename}"
        })
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        return response
    
    try:
        print("Processing image with super-resolution model")
        # Process the image with the enhanced super-resolution model
        _, sr_img = process_image_advanced(original_path, model)
        
        # Save the improved image
        improved_filename = f"improved_{original_filename}"
        improved_path = os.path.join(app.config['UPLOAD_FOLDER'], 'improved', improved_filename)
        cv2.imwrite(improved_path, sr_img)
        print(f"Improved image saved: {improved_filename}")
        
        response = jsonify({
            'success': True,
            'original_image': original_filename,
            'improved_image': f"improved/{improved_filename}"
        })
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        return response
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

@app.route('/api/images/<path:filename>')
def get_image(filename):
    print(f"Image request: {filename}")
    directory, file = os.path.split(filename)
    if directory:
        response = send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], directory), file)
    else:
        response = send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    return response

@app.route('/api/model_status')
def model_status():
    load_sr_model()
    response = jsonify({
        'model_loaded': model is not None,
        'model_path': MODEL_PATH
    })
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    return response

if __name__ == '__main__':
    load_sr_model()
    app.run(debug=True, port=5002, host='0.0.0.0')