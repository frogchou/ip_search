from fastapi import FastAPI, Body, HTTPException, Header, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import json
import sys
import os
from IpSearch_czdb import czdb_search

# 导入速率限制相关库
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# 设置默认编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 创建FastAPI应用
app = FastAPI()

# 配置速率限制器
limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

class InputData(BaseModel):
    point: str
    params: dict = {}

@app.post("/ip/ipsearch_for_dify")
async def ipsearch_for_dify(data: InputData = Body(...), authorization: str = Header(None)):
    expected_api_key = "123456"  # TODO: Replace with your actual API key
    auth_scheme, _, api_key = authorization.partition(' ')

    if auth_scheme.lower() != "bearer" or api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

    point = data.point

    if point == "ping":
        return {"result": "pong"}
    elif point == "app.external_data_tool.query":
        local_result=czdb_search(data.params['inputs']['ip_address']) 
        return {"result":"位置是："+str(local_result)}
    else:
        raise HTTPException(status_code=400, detail="Not implemented")

@app.get("/", response_class=PlainTextResponse)
async def get_client_ip(request: Request):
    client_ip = request.client.host
    return client_ip

@app.get("/api/ipsearch")
@limiter.limit("15/minute")  # 限制每分钟15次请求
async def api_ipsearch(ip: str, request: Request):
    """IP查询API端点"""
    try:
        result = czdb_search(ip)
        # 解析czdb_search返回的结果
        if result and len(result) >= 2:
            # 第一个元素包含国家、省份、城市等信息
            location_info = result[0].split('–')
            country = location_info[0] if location_info else '未知'
            province = location_info[1] if len(location_info) > 1 else '未知'
            city = location_info[2] if len(location_info) > 2 else '未知'
            district = location_info[3] if len(location_info) > 3 else '未知'
            
            # 第二个元素包含运营商信息
            isp = result[1]
            
            return {
                "ip": ip,
                "country": country,
                "province": province,
                "city": city,
                "district": district,
                "isp": isp
            }
        else:
            return {
                "ip": ip,
                "error": "未找到IP地址信息"
            }
    except Exception as e:
        return {
            "ip": ip,
            "error": str(e)
        }

@app.get("/api/ipdb/version")
async def get_ipdb_version():
    """获取IP数据库版本信息"""
    version_file = os.path.join("czdb", "version.txt")
    try:
        with open(version_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        version_info = {}
        for line in lines:
            if "更新时间:" in line:
                version_info["update_time"] = line.split("更新时间:")[1].strip()
            elif "版本号:" in line:
                version_info["version"] = line.split("版本号:")[1].strip()
        
        return JSONResponse(content=version_info)
    except FileNotFoundError:
        return JSONResponse(content={"update_time": "未知", "version": "未知"})
    except Exception as e:
        return JSONResponse(content={"update_time": "未知", "version": "未知", "error": str(e)})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)