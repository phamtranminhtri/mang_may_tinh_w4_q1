from flask import Flask, jsonify, request
import time
import os
import random
import string

app = Flask(__name__)

BACKEND_ID = os.getenv('BACKEND_ID', 'backend-1')
BACKEND_IP = os.getenv('BACKEND_IP', 'unknown')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'backend',
        'backend_id': BACKEND_ID,
        'ip': BACKEND_IP,
        'timestamp': time.time()
    })

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({
        'message': 'pong',
        'backend_id': BACKEND_ID,
        'timestamp': time.time()
    })

@app.route('/data', methods=['GET'])
def get_data():
    size_kb = request.args.get('size', default=100, type=int)
    # Giới hạn max 10MB để tránh quá tải
    size_kb = min(size_kb, 10240)
    
    # Tạo random string
    data_size = size_kb * 1024  # Convert to bytes
    random_data = ''.join(random.choices(string.ascii_letters + string.digits, k=data_size))
    
    return jsonify({
        'backend_id': BACKEND_ID,
        'data_size_kb': size_kb,
        'data': random_data,
        'timestamp': time.time()
    })

@app.route('/process', methods=['POST'])
def process_data():
    data = request.get_json()
    
    processing_time = data.get('delay', 0.1)
    time.sleep(processing_time)
    
    return jsonify({
        'backend_id': BACKEND_ID,
        'status': 'processed',
        'input': data,
        'processing_time': processing_time,
        'timestamp': time.time()
    })

@app.route('/metrics', methods=['GET'])
def metrics():
    import psutil
    
    return jsonify({
        'backend_id': BACKEND_ID,
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'timestamp': time.time()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
