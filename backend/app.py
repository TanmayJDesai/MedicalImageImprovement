import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)  

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        filename_parts = os.path.splitext(original_filename)
        unique_filename = f"{filename_parts[0]}_{str(uuid.uuid4())}{filename_parts[1]}"
        
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(original_path)
        
        return jsonify({
            'success': True,
            'original_image': unique_filename
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/api/improve', methods=['POST'])
def improve_image():
    data = request.json
    if not data or 'filename' not in data:
        return jsonify({'error': 'No filename provided'}), 400
    
    original_filename = data['filename']
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    
    if not os.path.exists(original_path):
        return jsonify({'error': 'Original image not found'}), 404
    
    improved_filename = f"improved_{original_filename}"
    improved_path = os.path.join(app.config['UPLOAD_FOLDER'], improved_filename)
    
    import shutil
    shutil.copy(original_path, improved_path)
    
    return jsonify({
        'success': True,
        'improved_image': improved_filename
    })

@app.route('/api/images/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)