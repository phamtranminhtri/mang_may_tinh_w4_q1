#!/usr/bin/env python3
"""
Script đo latency giữa frontend và backend
"""
import requests
import time
import statistics
import argparse

def measure_latency(frontend_url, count=100):
    """Gửi requests và đo latency"""
    print(f"Đo latency với {count} requests...")
    print(f"Frontend URL: {frontend_url}")
    print("-" * 60)
    
    latencies = []
    errors = 0
    
    for i in range(count):
        try:
            start = time.time()
            response = requests.get(f"{frontend_url}/call-backend", timeout=5)
            duration = (time.time() - start) * 1000  # ms
            
            if response.status_code == 200:
                latencies.append(duration)
                if (i + 1) % 10 == 0:
                    print(f"Progress: {i+1}/{count} - Current: {duration:.2f}ms")
            else:
                errors += 1
        except Exception as e:
            errors += 1
            print(f"Error at request {i+1}: {e}")
    
    # Tính toán thống kê
    if latencies:
        avg = statistics.mean(latencies)
        median = statistics.median(latencies)
        stdev = statistics.stdev(latencies) if len(latencies) > 1 else 0
        min_lat = min(latencies)
        max_lat = max(latencies)
        packet_loss = (errors / count) * 100
        
        print("\n" + "=" * 60)
        print("KẾT QUẢ ĐO LATENCY")
        print("=" * 60)
        print(f"Tổng requests:     {count}")
        print(f"Thành công:        {len(latencies)}")
        print(f"Lỗi:               {errors}")
        print(f"Packet loss:       {packet_loss:.2f}%")
        print("-" * 60)
        print(f"Latency trung bình: {avg:.2f} ms")
        print(f"Latency trung vị:   {median:.2f} ms")
        print(f"Độ lệch chuẩn:      {stdev:.2f} ms")
        print(f"Min latency:        {min_lat:.2f} ms")
        print(f"Max latency:        {max_lat:.2f} ms")
        print("=" * 60)
        
        return {
            'avg': avg,
            'median': median,
            'stdev': stdev,
            'min': min_lat,
            'max': max_lat,
            'packet_loss': packet_loss
        }
    else:
        print("\nKhông có request nào thành công!")
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Đo latency giữa frontend và backend')
    parser.add_argument('--url', default='http://localhost:8080', 
                        help='Frontend URL (default: http://localhost:8080)')
    parser.add_argument('--count', type=int, default=100,
                        help='Số lượng requests (default: 100)')
    
    args = parser.parse_args()
    measure_latency(args.url, args.count)
