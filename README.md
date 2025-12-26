# 纯真IP数据库查询服务

这是一个基于FastAPI的纯真IP数据库查询服务，提供IP地址查询功能，并支持每周自动更新数据库。

## 功能特性

- 🔍 **IP地址查询**：支持IPv4和IPv6地址查询
- 🔄 **自动更新**：每周自动更新纯真IP数据库社区版
- 🔒 **安全配置**：敏感信息存储在.env文件中
- 📊 **版本信息**：提供数据库版本信息查询
- ⚡ **快速响应**：基于FastAPI的高性能API服务
- 📱 **友好界面**：暗黑极客风格的Web界面

## 技术栈

- **后端框架**：FastAPI
- **数据库**：纯真IP数据库(czdb格式)
- **定时任务**：APScheduler
- **环境变量**：python-dotenv
- **Web界面**：HTML/CSS/JavaScript

## 安装和使用

### 1. 克隆项目

```bash
git clone <项目地址>
cd ip_search
```

### 2. 创建虚拟环境(可选)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制.env.example文件为.env，并填写相关配置：

```bash
cp .env.example .env
```

编辑.env文件：

```ini
# 纯真IP数据库下载地址
IPDB_DOWNLOAD_URL=https://www.cz88.net/api/communityIpAuthorization/communityIpDbFile?fn=czdb&key=YOUR_DOWNLOAD_KEY_HERE

# 数据库调用密钥
IPDB_API_KEY=YOUR_API_KEY_HERE

# 下载地址中的key参数
IPDB_DOWNLOAD_KEY=YOUR_DOWNLOAD_KEY_HERE
```

### 5. 启动服务

#### 启动API服务

```bash
python server.py
```

服务将在 http://0.0.0.0:8001 上运行。

#### 启动自动更新服务

```bash
python setup_cron.py
```

此服务将在后台运行，每周一凌晨2点自动更新IP数据库。

### 6. 访问服务

- Web界面：http://localhost:8001
- API接口：http://localhost:8001/api/ipsearch?ip=8.8.8.8
- 版本信息：http://localhost:8001/api/ipdb/version

## API使用说明

### IP查询接口

```
GET /api/ipsearch?ip=<IP地址>
```

**参数**：
- `ip`：要查询的IP地址(IPv4或IPv6)

**返回示例**：

```json
{
  "ip": "8.8.8.8",
  "country": "美国",
  "province": "",
  "city": "",
  "district": "",
  "isp": "Google LLC"
}
```

### 版本信息接口

```
GET /api/ipdb/version
```

**返回示例**：

```json
{
  "update_time": "2025-12-26 10:36:20",
  "version": "20251226"
}
```

## 项目结构

```
ip_search/
├── czdb/                   # IP数据库目录
│   ├── cz88_public_v4.czdb # IPv4数据库
│   ├── cz88_public_v6.czdb # IPv6数据库
│   └── version.txt         # 版本信息文件
├── static/                 # 静态文件目录
│   └── index.html          # 网页界面
├── .env                    # 环境变量配置(不提交到git)
├── .env.example            # 环境变量示例
├── .gitignore              # Git忽略文件
├── Dockerfile              # Docker配置
├── IpSearch_czdb.py        # IP查询模块
├── requirements.txt        # 依赖列表
├── server.py               # API服务
├── setup_cron.py           # 定时任务设置
├── update_ipdb.py          # 数据库更新脚本
└── README.md               # 项目说明
```

## 注意事项

1. **敏感信息保护**：.env文件包含敏感信息，不要将其提交到git仓库
2. **版本更新**：数据库每周一凌晨2点自动更新，也可以手动运行`python update_ipdb.py`更新
3. **API限流**：API接口限制每分钟15次请求，防止滥用
4. **跨平台支持**：支持Windows、Linux、Mac等操作系统

## Docker部署

### 构建镜像

```bash
docker build -t ip_search .
```

### 运行容器

```bash
docker run -d -p 8001:8001 ip_search
```

或使用docker-compose：

```bash
docker-compose up -d
```

## 开发说明

### 测试API

```bash
python test_api.py
```

### 测试速率限制

```bash
python test_rate_limit.py
```

## 贡献

欢迎提交Issue和Pull Request来改进项目。

## 许可证 （License）

MIT License
