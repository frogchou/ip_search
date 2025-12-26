import requests
import json

# 测试API端点
response = requests.get('http://localhost:8001/api/ipsearch?ip=8.8.8.8')
print(f"Status code: {response.status_code}")
print(f"Content type: {response.headers.get('Content-Type')}")
print(f"Response encoding: {response.encoding}")

# 尝试解析JSON数据
json_data = response.json()
print(f"JSON response: {json.dumps(json_data, ensure_ascii=False, indent=2)}")

# 测试其他IP
response2 = requests.get('http://localhost:8001/api/ipsearch?ip=114.114.114.114')
json_data2 = response2.json()
print(f"\nJSON response for 114.114.114.114: {json.dumps(json_data2, ensure_ascii=False, indent=2)}")
