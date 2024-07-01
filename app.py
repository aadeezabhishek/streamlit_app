from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from tqdm import tqdm  # Ensure tqdm is installed (`pip install tqdm`)
from document_processor import process_file, summarize_chunks, generate_final_response
from flask_socketio import SocketIO, emit
import threading
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
socketio = SocketIO(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(file_path)

    # Start the processing in a separate thread
    thread = threading.Thread(target=process_and_summarize, args=(file_path,))
    thread.start()

    return jsonify({'message': 'File uploaded successfully! Processing started.'})

def process_and_summarize(file_path):
    socketio.emit('progress', {'progress': 10, 'message': 'File uploaded. Starting processing.'})
    
    # Simulate processing time
    time.sleep(2)  # Simulate some delay for chunking
    chunks = process_file(file_path)
    socketio.emit('progress', {'progress': 30, 'message': 'File chunked. Starting summary generation.'})
    
    summaries = summarize_chunks(chunks)
    socketio.emit('progress', {'progress': 60, 'message': 'Summaries generated. Creating final response.'})

    combined_summary = "\n\n".join(summaries.values())
    response = generate_final_response(combined_summary)
    
    socketio.emit('progress', {'progress': 100, 'message': 'Processing complete.', 'summary': response})

if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False, port=8506)
