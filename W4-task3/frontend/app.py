from flask import Flask, jsonify, request
import requests
import time
import os

app = Flask(__name__)

# Backend URL sẽ thay đổi tùy theo phương pháp networking
# Có thể set qua biến môi trường
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'frontend',
        'backend_url': BACKEND_URL,
        'timestamp': time.time()
    })

@app.route('/call-backend', methods=['GET'])
def call_backend():
    """
    Gọi backend và trả kết quả
    Dùng để test kết nối giữa frontend và backend
    """
    try:
        start_time = time.time()
        response = requests.get(f'{BACKEND_URL}/ping', timeout=5)
        latency = (time.time() - start_time) * 1000  # ms
        
        return jsonify({
            'status': 'success',
            'backend_response': response.json(),
            'latency_ms': round(latency, 2),
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': time.time()
        }), 500

@app.route('/test-throughput', methods=['GET'])
def test_throughput():
    """
    Test throughput bằng cách download data từ backend
    Query param: size (KB)
    """
    size_kb = request.args.get('size', default=100, type=int)
    
    try:
        start_time = time.time()
        response = requests.get(f'{BACKEND_URL}/data?size={size_kb}', timeout=30)
        duration = time.time() - start_time
        
        # Tính throughput
        data_size_mb = size_kb / 1024
        throughput_mbps = (data_size_mb * 8) / duration if duration > 0 else 0
        
        return jsonify({
            'status': 'success',
            'data_size_kb': size_kb,
            'duration_seconds': round(duration, 3),
            'throughput_mbps': round(throughput_mbps, 2),
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': time.time()
        }), 500

@app.route('/test-latency', methods=['GET'])
def test_latency():
    """
    Đo latency bằng cách gửi nhiều requests liên tiếp
    Query param: count (số lần ping, mặc định 10)
    """
    count = request.args.get('count', default=10, type=int)
    count = min(count, 1000)  # Giới hạn max 1000
    
    latencies = []
    errors = 0
    
    for i in range(count):
        try:
            start_time = time.time()
            response = requests.get(f'{BACKEND_URL}/ping', timeout=5)
            latency = (time.time() - start_time) * 1000
            latencies.append(latency)
        except:
            errors += 1
    
    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        packet_loss = (errors / count) * 100
    else:
        avg_latency = min_latency = max_latency = 0
        packet_loss = 100
    
    return jsonify({
        'status': 'success',
        'test_count': count,
        'successful': len(latencies),
        'errors': errors,
        'packet_loss_percent': round(packet_loss, 2),
        'avg_latency_ms': round(avg_latency, 2),
        'min_latency_ms': round(min_latency, 2),
        'max_latency_ms': round(max_latency, 2),
        'all_latencies': [round(l, 2) for l in latencies[:100]],  # Chỉ trả 100 đầu
        'timestamp': time.time()
    })

@app.route('/process', methods=['POST'])
def process():
    """Forward request tới backend để xử lý"""
    try:
        data = request.get_json()
        response = requests.post(f'{BACKEND_URL}/process', json=data, timeout=10)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Chạy trên port 8080
    app.run(host='0.0.0.0', port=8080, debug=False)
