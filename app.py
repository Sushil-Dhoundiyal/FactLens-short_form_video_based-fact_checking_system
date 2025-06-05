

from flask import Flask, request, jsonify, render_template, session
from werkzeug.utils import secure_filename
import os
import subprocess
import json

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "data")
app.secret_key = 'SET YOUR SECRET KEY'  # 🔑 Required for sessions

ALLOWED_EXT = {'mp4', 'mov', 'avi', 'mkv'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(os.getcwd(), "outputs"), exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/policies')
def policies():
    return render_template('policies.html')

@app.route('/safety')
def safety():
    return render_template('safety.html')

@app.route('/trending')
def trending():
    return render_template('trending.html')

@app.route('/process-video', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No file'}), 400

    file = request.files['video']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400

    # Save the uploaded video to data/test_video.mp4
    filename = secure_filename('test_video.mp4')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Run your backend pipeline
    try:
        subprocess.run(['python', 'run.py'], check=True)
    except subprocess.CalledProcessError:
        return jsonify({'error': 'Processing failed'}), 500

    try:
        with open('outputs/verified_claims.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        session['results'] = results  # ✅ Save results in session
        return jsonify(results), 200

    except FileNotFoundError:
        return jsonify({'error': 'Result file not found'}), 500

@app.route('/get-session-results', methods=['GET'])
def get_session_results():
    results = session.get('results')
    if results:
        return jsonify(results), 200
    else:
        return jsonify({'error': 'No session results'}), 404

if __name__ == '__main__':
    app.run(debug=True)
