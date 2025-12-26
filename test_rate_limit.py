import requests
import time

# 测试IP地址
TEST_IP = "8.8.8.8"
API_URL = f"http://localhost:8001/api/ipsearch?ip={TEST_IP}"

print("开始测试速率限制功能...")
print(f"将向 {API_URL} 发送20个连续请求")
print("-" * 60)

# 连续发送20个请求
for i in range(1, 21):
    start_time = time.time()
    try:
        response = requests.get(API_URL)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # 毫秒
        
        print(f"请求 #{i}: 状态码 = {response.status_code}, 响应时间 = {response_time:.2f}ms")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  响应: {data['ip']} - {data['country']} {data['province']}")
        elif response.status_code == 429:
            print(f"  响应: {response.json()}")
        else:
            print(f"  响应: {response.text}")
            
    except Exception as e:
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        print(f"请求 #{i}: 发生错误 - {e}, 响应时间 = {response_time:.2f}ms")
    
    print("-" * 60)

print("速率限制测试完成!")