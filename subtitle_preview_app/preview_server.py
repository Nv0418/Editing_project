from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import sys
import time

app = Flask(__name__)
CORS(app)

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@app.route('/generate-preview', methods=['POST'])
def generate_preview():
    try:
        data = request.json
        style = data.get('style', 'simple_caption')
        text = data.get('text', 'SAMPLE TEXT')
        
        print(f"[Flask Server] Received request: style='{style}', text='{text}'") # Log received text
        
        # Run the style preview generator
        cmd = [
            'python3',
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'style_preview_generator.py'),
            '--style', style,
            '--text', text
        ]
        
        print(f"[Flask Server] Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        
        print(f"[Flask Server] Subprocess stdout: {result.stdout}") # Log script stdout
        print(f"[Flask Server] Subprocess stderr: {result.stderr}") # Log script stderr

        if result.returncode != 0:
            print(f"[Flask Server] Error generating preview. Return code: {result.returncode}")
            return jsonify({'error': 'Failed to generate preview', 'details': result.stderr}), 500
        
        # Wait a moment for file to be written
        time.sleep(0.5)
        
        # Return the preview image path with absolute path for serving
        preview_filename = f'{style}_preview.png'
        preview_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'style_previews', preview_filename)
        
        # Check if file exists
        if not os.path.exists(preview_path):
            return jsonify({'error': 'Preview file not found'}), 404
            
        # Return URL that Flask will serve
        return jsonify({
            'success': True,
            'preview_url': f'/serve-preview/{preview_filename}',
            'timestamp': int(time.time() * 1000)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/serve-preview/<filename>')
def serve_preview(filename):
    # Serve preview images directly from Flask to avoid caching issues
    preview_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'style_previews', filename)
    
    if not os.path.exists(preview_path):
        return jsonify({'error': 'Preview not found'}), 404
        
    # Add cache control headers to prevent browser caching
    response = send_file(preview_path, mimetype='image/png')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(port=5001, debug=False)
