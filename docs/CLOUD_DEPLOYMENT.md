# SparkBox 云服务器部署完整指南

## 🎯 部署目标

将 SparkBox 部署到云服务器，实现：
- 24小时在线访问
- 独立域名访问
- HTTPS 安全连接
- 自动备份数据

---

## 📋 准备工作

### 1. 购买云服务器

#### 阿里云（推荐国内用户）

1. 访问 https://www.aliyun.com/
2. 选择"云服务器 ECS"
3. 推荐配置：
   - 地域：选择离你最近的
   - 实例规格：1核2GB（约¥99/年）
   - 镜像：Ubuntu 20.04 64位
   - 网络：按使用流量计费
   - 安全组：开放 22, 80, 443 端口

#### 腾讯云（学生优惠）

1. 访问 https://cloud.tencent.com/
2. 学生认证后可享受 ¥10/月
3. 配置同上

#### DigitalOcean（推荐国外用户）

1. 访问 https://www.digitalocean.com/
2. 创建 Droplet
3. 选择 $6/月 套餐
4. 选择 Ubuntu 20.04
5. 选择离你最近的数据中心

### 2. 购买域名（可选但推荐）

**国内**:
- 阿里云万网：https://wanwang.aliyun.com/
- 腾讯云 DNSPod：https://dnspod.cloud.tencent.com/
- 价格：¥30-60/年（.com/.cn）

**国外**:
- Namecheap：https://www.namecheap.com/
- GoDaddy：https://www.godaddy.com/
- 价格：$10-15/年

### 3. 本地准备

```bash
# 安装 SSH 客户端（Windows 用户）
# 下载 PuTTY: https://www.putty.org/

# 或使用 Windows Terminal + OpenSSH
```

---

## 🔧 服务器初始化

### 1. 连接服务器

```bash
# 使用 SSH 连接（替换为你的服务器 IP）
ssh root@your-server-ip

# 首次连接会提示保存指纹，输入 yes
# 输入密码（购买时设置的）
```

### 2. 更新系统

```bash
# 更新软件包列表
apt update

# 升级已安装的软件包
apt upgrade -y

# 安装必要工具
apt install -y git curl wget vim ufw
```

### 3. 创建新用户（安全考虑）

```bash
# 创建用户
adduser sparkbox

# 添加到 sudo 组
usermod -aG sudo sparkbox

# 切换到新用户
su - sparkbox
```

### 4. 配置防火墙

```bash
# 允许 SSH
sudo ufw allow 22/tcp

# 允许 HTTP
sudo ufw allow 80/tcp

# 允许 HTTPS
sudo ufw allow 443/tcp

# 启用防火墙
sudo ufw enable

# 查看状态
sudo ufw status
```

---

## 📦 安装依赖

### 1. 安装 Python 3.9+

```bash
# 安装 Python 和 pip
sudo apt install -y python3.9 python3.9-venv python3-pip

# 验证安装
python3.9 --version
```

### 2. 安装 Node.js

```bash
# 安装 Node.js 16.x
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install -y nodejs

# 验证安装
node --version
npm --version
```

### 3. 安装 Nginx

```bash
# 安装 Nginx
sudo apt install -y nginx

# 启动 Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# 验证安装
sudo systemctl status nginx
```

---

## 🚀 部署应用

### 1. 上传代码

#### 方法一：使用 Git（推荐）

```bash
# 在服务器上
cd ~
git clone https://github.com/yourusername/sparkbox.git
cd sparkbox
```

#### 方法二：使用 SCP 上传

```bash
# 在本地电脑上
# 压缩项目（排除不必要的文件）
cd d:\Cursor
tar -czf sparkbox.tar.gz sparkbox \
  --exclude=sparkbox/backend/venv \
  --exclude=sparkbox/backend/__pycache__ \
  --exclude=sparkbox/frontend/node_modules \
  --exclude=sparkbox/frontend/dist

# 上传到服务器
scp sparkbox.tar.gz sparkbox@your-server-ip:~/

# 在服务器上解压
ssh sparkbox@your-server-ip
tar -xzf sparkbox.tar.gz
cd sparkbox
```

### 2. 配置后端

```bash
cd ~/sparkbox/backend

# 创建虚拟环境
python3.9 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 安装 Gunicorn（生产环境服务器）
pip install gunicorn

# 创建 .env 文件
cat > .env << EOF
DATABASE_URL=sqlite:///./sparkbox.db
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI 服务配置（填入你的 API Key）
DEEPSEEK_API_KEY=your-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
EOF

# 测试启动
gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001
# 按 Ctrl+C 停止
```

### 3. 配置前端

```bash
cd ~/sparkbox/frontend

# 安装依赖
npm install

# 修改 API 地址
# 编辑 src/utils/api.js
vim src/utils/api.js
# 将 BASE_URL 改为：
# const BASE_URL = '/api/v1'

# 构建生产版本
npm run build

# 构建完成后，dist 目录包含所有静态文件
```

---

## 🔧 配置 Systemd 服务

### 1. 创建后端服务

```bash
sudo vim /etc/systemd/system/sparkbox-backend.service
```

写入以下内容：

```ini
[Unit]
Description=SparkBox Backend Service
After=network.target

[Service]
Type=notify
User=sparkbox
WorkingDirectory=/home/sparkbox/sparkbox/backend
Environment="PATH=/home/sparkbox/sparkbox/backend/venv/bin"
ExecStart=/home/sparkbox/sparkbox/backend/venv/bin/gunicorn main:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8001 \
  --access-logfile /home/sparkbox/sparkbox/backend/access.log \
  --error-logfile /home/sparkbox/sparkbox/backend/error.log
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
# 重新加载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start sparkbox-backend

# 设置开机自启
sudo systemctl enable sparkbox-backend

# 查看状态
sudo systemctl status sparkbox-backend

# 查看日志
sudo journalctl -u sparkbox-backend -f
```

---

## 🌐 配置 Nginx

### 1. 创建 Nginx 配置

```bash
sudo vim /etc/nginx/sites-available/sparkbox
```

写入以下内容：

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名或服务器 IP

    # 前端静态文件
    location / {
        root /home/sparkbox/sparkbox/frontend/dist;
        try_files $uri $uri/ /index.html;
        
        # 缓存静态资源
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # 后端 API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:8001/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # API 文档
    location /docs {
        proxy_pass http://127.0.0.1:8001/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 日志
    access_log /var/log/nginx/sparkbox_access.log;
    error_log /var/log/nginx/sparkbox_error.log;
}
```

### 2. 启用配置

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/sparkbox /etc/nginx/sites-enabled/

# 删除默认配置
sudo rm /etc/nginx/sites-enabled/default

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

---

## 🔒 配置 HTTPS（推荐）

### 1. 安装 Certbot

```bash
# 安装 Certbot
sudo apt install -y certbot python3-certbot-nginx
```

### 2. 获取 SSL 证书

```bash
# 自动配置 HTTPS（替换为你的域名和邮箱）
sudo certbot --nginx -d your-domain.com -d www.your-domain.com --email your-email@example.com --agree-tos --no-eff-email

# 测试自动续期
sudo certbot renew --dry-run
```

### 3. 自动续期

```bash
# Certbot 会自动添加续期任务到 cron
# 查看续期任务
sudo systemctl list-timers | grep certbot
```

---

## 🗄️ 配置数据库备份

### 1. 创建备份脚本

```bash
vim ~/backup-sparkbox.sh
```

写入以下内容：

```bash
#!/bin/bash

# 配置
BACKUP_DIR="/home/sparkbox/backups"
DB_FILE="/home/sparkbox/sparkbox/backend/sparkbox.db"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
cp $DB_FILE $BACKUP_DIR/sparkbox_$DATE.db

# 压缩备份
gzip $BACKUP_DIR/sparkbox_$DATE.db

# 保留最近30天的备份
find $BACKUP_DIR -name "sparkbox_*.db.gz" -mtime +30 -delete

echo "Backup completed: sparkbox_$DATE.db.gz"
```

```bash
# 添加执行权限
chmod +x ~/backup-sparkbox.sh

# 测试备份
~/backup-sparkbox.sh
```

### 2. 设置定时备份

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天凌晨2点备份）
0 2 * * * /home/sparkbox/backup-sparkbox.sh >> /home/sparkbox/backup.log 2>&1
```

---

## 🔍 监控和维护

### 1. 查看服务状态

```bash
# 查看后端服务
sudo systemctl status sparkbox-backend

# 查看 Nginx
sudo systemctl status nginx

# 查看日志
sudo journalctl -u sparkbox-backend -f
tail -f /var/log/nginx/sparkbox_access.log
```

### 2. 重启服务

```bash
# 重启后端
sudo systemctl restart sparkbox-backend

# 重启 Nginx
sudo systemctl restart nginx
```

### 3. 更新应用

```bash
# 拉取最新代码
cd ~/sparkbox
git pull

# 更新后端
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart sparkbox-backend

# 更新前端
cd ../frontend
npm install
npm run build
sudo systemctl restart nginx
```

---

## 📊 性能优化

### 1. 配置 Nginx 缓存

```nginx
# 在 /etc/nginx/nginx.conf 的 http 块中添加
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=100m inactive=60m;
```

### 2. 启用 Gzip 压缩

```nginx
# 在 server 块中添加
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
```

### 3. 配置日志轮转

```bash
sudo vim /etc/logrotate.d/sparkbox
```

```
/home/sparkbox/sparkbox/backend/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 sparkbox sparkbox
    sharedscripts
    postrotate
        systemctl reload sparkbox-backend > /dev/null 2>&1 || true
    endscript
}
```

---

## ✅ 验证部署

### 1. 检查服务

```bash
# 检查后端
curl http://localhost:8001/docs

# 检查前端
curl http://localhost/
```

### 2. 浏览器访问

- 访问：http://your-domain.com 或 http://your-server-ip
- 注册账号
- 创建想法
- 生成回顾

### 3. 检查 HTTPS

- 访问：https://your-domain.com
- 查看浏览器地址栏是否显示锁图标

---

## 🐛 常见问题

### 1. 后端无法启动

```bash
# 查看日志
sudo journalctl -u sparkbox-backend -n 50

# 检查端口占用
sudo netstat -tulpn | grep 8001

# 检查权限
ls -la /home/sparkbox/sparkbox/backend/
```

### 2. Nginx 502 错误

```bash
# 检查后端是否运行
sudo systemctl status sparkbox-backend

# 检查 Nginx 配置
sudo nginx -t

# 查看 Nginx 错误日志
sudo tail -f /var/log/nginx/sparkbox_error.log
```

### 3. 数据库权限问题

```bash
# 修改数据库文件权限
sudo chown sparkbox:sparkbox /home/sparkbox/sparkbox/backend/sparkbox.db
sudo chmod 644 /home/sparkbox/sparkbox/backend/sparkbox.db
```

---

## 📞 获取帮助

如遇到问题：
1. 查看日志文件
2. 检查服务状态
3. 参考文档
4. 提交 Issue

---

**部署完成！** 🎉

你的 SparkBox 现在已经在云端运行了！
