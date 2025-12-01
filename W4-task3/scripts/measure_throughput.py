#!/usr/bin/env python3
"""
Script đo throughput giữa frontend và backend
"""
import requests
import time
import argparse

def measure_throughput(frontend_url, size_kb=1024, iterations=10):
    """Đo throughput bằng cách download data nhiều lần"""
    print(f"Đo throughput với data size {size_kb}KB, {iterations} lần...")
    print(f"Frontend URL: {frontend_url}")
    print("-" * 60)
    
    throughputs = []
    
    for i in range(iterations):
        try:
            start = time.time()
            response = requests.get(
                f"{frontend_url}/test-throughput?size={size_kb}", 
                timeout=30
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                throughput = data.get('throughput_mbps', 0)
                throughputs.append(throughput)
                print(f"Iteration {i+1}/{iterations}: {throughput:.2f} Mbps "
                      f"(duration: {duration:.2f}s)")
            else:
                print(f"Error at iteration {i+1}: Status {response.status_code}")
        except Exception as e:
            print(f"Error at iteration {i+1}: {e}")
    
    # Tính toán
    if throughputs:
        avg_throughput = sum(throughputs) / len(throughputs)
        min_throughput = min(throughputs)
        max_throughput = max(throughputs)
        
        print("\n" + "=" * 60)
        print("KẾT QUẢ ĐO THROUGHPUT")
        print("=" * 60)
        print(f"Data size:          {size_kb} KB")
        print(f"Iterations:         {iterations}")
        print(f"Successful:         {len(throughputs)}")
        print("-" * 60)
        print(f"Avg throughput:     {avg_throughput:.2f} Mbps")
        print(f"Min throughput:     {min_throughput:.2f} Mbps")
        print(f"Max throughput:     {max_throughput:.2f} Mbps")
        print("=" * 60)
        
        return {
            'avg': avg_throughput,
            'min': min_throughput,
            'max': max_throughput
        }
    else:
        print("\nKhông có test nào thành công!")
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Đo throughput')
    parser.add_argument('--url', default='http://localhost:8080',
                        help='Frontend URL')
    parser.add_argument('--size', type=int, default=1024,
                        help='Data size in KB (default: 1024)')
    parser.add_argument('--iterations', type=int, default=10,
                        help='Number of iterations (default: 10)')
    
    args = parser.parse_args()
    measure_throughput(args.url, args.size, args.iterations)
