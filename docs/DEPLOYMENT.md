# SparkBox 部署指南 v1.0

## 📋 部署前准备

### 系统要求
- **操作系统**: Linux (推荐 Ubuntu 20.04+) / Windows / macOS
- **Python**: 3.9+
- **Node.js**: 16+
- **数据库**: SQLite 3
- **内存**: 至少 1GB
- **磁盘**: 至少 2GB

### 域名和 SSL（可选）
- 域名（如需公网访问）
- SSL 证书（推荐使用 Let's Encrypt）

## 🐳 Docker 部署（推荐）

### 1. 安装 Docker 和 Docker Compose

```bash
# Ubuntu
sudo apt update
sudo apt install docker.io docker-compose

# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker
```

### 2. 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: sparkbox-backend
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=sqlite:///./sparkbox.db
      - SECRET_KEY=${SECRET_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    volumes:
      - ./backend/sparkbox.db:/app/sparkbox.db
    restart: unless-stopped

  frontend:
    build: ./frontend
    container_name: sparkbox-frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: sparkbox-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
```

### 3. 创建后端 Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### 4. 创建前端 Dockerfile

```dockerfile
# frontend/Dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

### 5. 创建 .env 文件

```bash
# .env
SECRET_KEY=your-secret-key-here
DEEPSEEK_API_KEY=your-deepseek-api-key
```

### 6. 启动服务

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 🖥️ 传统部署

### 后端部署

#### 1. 安装依赖

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

#### 2. 配置环境变量

```bash
# 创建 .env 文件
cat > .env << EOF
DATABASE_URL=sqlite:///./sparkbox.db
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI 服务配置
DEEPSEEK_API_KEY=your-api-key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
EOF
```

#### 3. 初始化数据库

```bash
# 数据库会在首次运行时自动创建
python -c "from core.database import init_db; init_db()"
```

#### 4. 使用 Gunicorn 运行（生产环境）

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动服务
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8001 \
  --access-logfile - \
  --error-logfile -
```

#### 5. 使用 Systemd 管理服务

```bash
# 创建服务文件
sudo nano /etc/systemd/system/sparkbox-backend.service
```

```ini
[Unit]
Description=SparkBox Backend
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/sparkbox/backend
Environment="PATH=/path/to/sparkbox/backend/venv/bin"
ExecStart=/path/to/sparkbox/backend/venv/bin/gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8001

[Install]
WantedBy=multi-user.target
```

```bash
# 启动服务
sudo systemctl daemon-reload
sudo systemctl start sparkbox-backend
sudo systemctl enable sparkbox-backend

# 查看状态
sudo systemctl status sparkbox-backend
```

### 前端部署

#### 1. 构建生产版本

```bash
cd frontend

# 安装依赖
npm install

# 修改 API 地址（如需要）
# 编辑 src/utils/api.js
# const BASE_URL = 'https://your-domain.com/api/v1'

# 构建
npm run build
```

#### 2. 使用 Nginx 部署

```bash
# 安装 Nginx
sudo apt install nginx

# 创建配置文件
sudo nano /etc/nginx/sites-available/sparkbox
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/sparkbox/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api/ {
        proxy_pass http://localhost:8001/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# 启用站点
sudo ln -s /etc/nginx/sites-available/sparkbox /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

#### 3. 配置 SSL（推荐）

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

## 🔧 配置优化

### 后端优化

#### 1. 数据库优化

```python
# core/database.py
# 添加连接池配置
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

#### 2. 日志配置

```python
# main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sparkbox.log'),
        logging.StreamHandler()
    ]
)
```

### 前端优化

#### 1. 构建优化

```javascript
// vite.config.js
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          'ui-vendor': ['html2canvas']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  }
})
```

#### 2. Nginx 缓存配置

```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## 📊 监控和维护

### 1. 日志管理

```bash
# 查看后端日志
tail -f /path/to/sparkbox/backend/sparkbox.log

# 查看 Nginx 日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 2. 数据库备份

```bash
# 创建备份脚本
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/path/to/backups"
DB_FILE="/path/to/sparkbox/backend/sparkbox.db"

mkdir -p $BACKUP_DIR
cp $DB_FILE $BACKUP_DIR/sparkbox_$DATE.db

# 保留最近30天的备份
find $BACKUP_DIR -name "sparkbox_*.db" -mtime +30 -delete
EOF

chmod +x backup.sh

# 添加到 crontab（每天凌晨2点备份）
crontab -e
# 添加: 0 2 * * * /path/to/backup.sh
```

### 3. 性能监控

```bash
# 安装监控工具
pip install prometheus-fastapi-instrumentator

# 在 main.py 中添加
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

## 🔒 安全加固

### 1. 防火墙配置

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. 限制访问

```nginx
# Nginx 限流配置
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

location /api/ {
    limit_req zone=api burst=20 nodelay;
    # ... 其他配置
}
```

### 3. 定期更新

```bash
# 更新系统
sudo apt update && sudo apt upgrade

# 更新 Python 依赖
pip install --upgrade -r requirements.txt

# 更新 Node 依赖
npm update
```

## 🐛 故障排查

### 常见问题

1. **后端无法启动**
   - 检查端口是否被占用：`netstat -tulpn | grep 8001`
   - 检查环境变量是否正确配置
   - 查看日志文件

2. **前端无法访问后端**
   - 检查 CORS 配置
   - 检查 Nginx 代理配置
   - 检查防火墙规则

3. **数据库错误**
   - 检查数据库文件权限
   - 检查磁盘空间
   - 尝试重建数据库

4. **AI 生成失败**
   - 检查 API Key 是否正确
   - 检查网络连接
   - 查看 AI 服务状态

## 📞 技术支持

如遇到部署问题，请：
1. 查看日志文件
2. 检查配置文件
3. 参考文档
4. 提交 Issue

---

**祝部署顺利！** 🚀
