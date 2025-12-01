#!/usr/bin/env python3
"""
Test stability - chạy requests liên tục trong một khoảng thời gian
"""
import requests
import time
import argparse
from datetime import datetime

def test_stability(frontend_url, duration_minutes=5):
    """Test stability trong một khoảng thời gian"""
    print(f"Test stability trong {duration_minutes} phút...")
    print(f"Frontend URL: {frontend_url}")
    print(f"Bắt đầu: {datetime.now()}")
    print("-" * 60)
    
    end_time = time.time() + (duration_minutes * 60)
    total_requests = 0
    successful_requests = 0
    errors = 0
    timeouts = 0
    
    latencies = []
    
    while time.time() < end_time:
        total_requests += 1
        
        try:
            start = time.time()
            response = requests.get(f"{frontend_url}/call-backend", timeout=5)
            duration = (time.time() - start) * 1000
            
            if response.status_code == 200:
                successful_requests += 1
                latencies.append(duration)
            else:
                errors += 1
                
        except requests.exceptions.Timeout:
            timeouts += 1
        except Exception as e:
            errors += 1
        
        # In progress mỗi 30 giây
        if total_requests % 30 == 0:
            success_rate = (successful_requests / total_requests) * 100
            print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                  f"Requests: {total_requests}, Success: {successful_requests}, "
                  f"Success rate: {success_rate:.1f}%")
        
        # Delay nhỏ giữa các requests
        time.sleep(1)
    
    # Kết quả
    success_rate = (successful_requests / total_requests) * 100 if total_requests > 0 else 0
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    
    print("\n" + "=" * 60)
    print("KẾT QUẢ TEST STABILITY")
    print("=" * 60)
    print(f"Duration:           {duration_minutes} phút")
    print(f"Total requests:     {total_requests}")
    print(f"Successful:         {successful_requests}")
    print(f"Errors:             {errors}")
    print(f"Timeouts:           {timeouts}")
    print(f"Success rate:       {success_rate:.2f}%")
    print(f"Avg latency:        {avg_latency:.2f} ms")
    print("=" * 60)
    
    return {
        'total': total_requests,
        'successful': successful_requests,
        'errors': errors,
        'timeouts': timeouts,
        'success_rate': success_rate,
        'avg_latency': avg_latency
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test stability')
    parser.add_argument('--url', default='http://localhost:8080',
                        help='Frontend URL')
    parser.add_argument('--duration', type=int, default=5,
                        help='Duration in minutes (default: 5)')
    
    args = parser.parse_args()
    test_stability(args.url, args.duration)
