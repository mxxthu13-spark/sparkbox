# SparkBox Vercel 快速部署指南

## 🎯 目标：今天内上线！

**预计时间**：2-3小时  
**成本**：完全免费  
**难度**：⭐⭐（简单）

---

## 📋 部署清单

- [ ] 准备 GitHub 账号
- [ ] 准备 Vercel 账号（已有 ✅）
- [ ] 准备 Railway 账号
- [ ] 上传代码到 GitHub
- [ ] 部署后端到 Railway
- [ ] 部署前端到 Vercel
- [ ] 连接前后端
- [ ] 测试功能
- [ ] 完成上线！

---

## ⏱️ 时间规划

| 步骤 | 时间 | 说明 |
|------|------|------|
| 准备工作 | 10分钟 | 注册账号 |
| 代码准备 | 20分钟 | 上传到 GitHub |
| 部署后端 | 30分钟 | Railway 部署 |
| 部署前端 | 20分钟 | Vercel 部署 |
| 连接测试 | 30分钟 | 联调测试 |
| **总计** | **约2小时** | **今天完成** |

---

## 🚀 详细步骤

### 第一步：准备工作（10分钟）

#### 1. 注册 GitHub（如果没有）

访问：https://github.com/signup
- 填写邮箱
- 创建密码
- 验证邮箱

#### 2. 注册 Railway（如果没有）

访问：https://railway.app/
- 点击 "Login"
- 选择 "Login with GitHub"
- 授权 Railway 访问 GitHub

#### 3. 准备 AI API Key

**DeepSeek（推荐，便宜）**：
- 访问：https://platform.deepseek.com/
- 注册账号
- 充值（最低 ¥10）
- 创建 API Key
- 复制保存

**或 Qwen（阿里云）**：
- 访问：https://dashscope.aliyun.com/
- 注册账号
- 开通服务
- 创建 API Key

---

### 第二步：准备代码（20分钟）

#### 1. 创建 .gitignore 文件

在 `d:\Cursor\sparkbox\` 目录下创建 `.gitignore`：

```bash
# 在项目根目录
cd d:\Cursor\sparkbox
```

创建 `.gitignore` 文件，内容如下：

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Node
node_modules/
dist/
.DS_Store

# 数据库
*.db
*.sqlite
*.sqlite3

# 环境变量
.env
.env.local

# 日志
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# 临时文件
*.tmp
.cache/

# 备份文件
*.bak
backup*/
```

#### 2. 修改前端 API 地址

编辑 `frontend/src/utils/api.js`：

```javascript
// 修改这一行
const BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

// 其他代码保持不变
```

#### 3. 创建前端环境变量文件

在 `frontend/` 目录创建 `.env.example`：

```bash
# API 地址（部署后会替换）
VITE_API_URL=https://your-backend.railway.app/api/v1
```

#### 4. 修改后端 requirements.txt

确保 `backend/requirements.txt` 包含 gunicorn：

```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.1.1
httpx==0.25.2
python-multipart==0.0.6
gunicorn==21.2.0
```

#### 5. 创建后端 Procfile

在 `backend/` 目录创建 `Procfile`（无扩展名）：

```
web: gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

---

### 第三步：上传到 GitHub（15分钟）

#### 1. 初始化 Git 仓库

```bash
# 进入项目目录
cd d:\Cursor\sparkbox

# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "SparkBox v1.0 - Initial commit"
```

#### 2. 创建 GitHub 仓库

1. 访问：https://github.com/new
2. Repository name: `sparkbox`
3. Description: `思想记录与 AI 回顾工具`
4. 选择 Public 或 Private
5. 不要勾选任何初始化选项
6. 点击 "Create repository"

#### 3. 推送代码

```bash
# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/sparkbox.git

# 推送代码
git branch -M main
git push -u origin main
```

如果推送失败，可能需要配置 Git：

```bash
# 配置用户名和邮箱
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 如果需要认证，使用 Personal Access Token
# 访问：https://github.com/settings/tokens
# 生成 token，然后使用 token 作为密码
```

---

### 第四步：部署后端到 Railway（30分钟）

#### 1. 创建新项目

1. 访问：https://railway.app/dashboard
2. 点击 "New Project"
3. 选择 "Deploy from GitHub repo"
4. 选择 `sparkbox` 仓库
5. 选择 `backend` 目录

#### 2. 配置环境变量

在 Railway 项目中：
1. 点击项目
2. 点击 "Variables" 标签
3. 添加以下环境变量：

```bash
# 数据库
DATABASE_URL=sqlite:///./sparkbox.db

# JWT 密钥（生成一个随机字符串）
SECRET_KEY=your-secret-key-here-make-it-long-and-random

# JWT 配置
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI 服务（DeepSeek）
DEEPSEEK_API_KEY=your-deepseek-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat

# 或使用 Qwen
# QWEN_API_KEY=your-qwen-api-key-here
# QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
# QWEN_MODEL=qwen-plus

# 端口（Railway 会自动设置）
PORT=8001
```

**生成 SECRET_KEY**：
```bash
# 在命令行运行
python -c "import secrets; print(secrets.token_hex(32))"

# 或在线生成
# https://www.random.org/strings/
```

#### 3. 配置构建设置

1. 点击 "Settings" 标签
2. 找到 "Build" 部分
3. Root Directory: `backend`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

#### 4. 部署

1. 点击 "Deploy"
2. 等待部署完成（3-5分钟）
3. 部署成功后，点击 "Generate Domain"
4. 复制域名，例如：`sparkbox-backend-production.up.railway.app`

#### 5. 测试后端

访问：`https://your-backend-domain.railway.app/docs`

应该能看到 API 文档页面。

---

### 第五步：部署前端到 Vercel（20分钟）

#### 1. 导入项目

1. 访问：https://vercel.com/dashboard
2. 点击 "Add New..." -> "Project"
3. 选择 "Import Git Repository"
4. 选择你的 `sparkbox` 仓库
5. 点击 "Import"

#### 2. 配置项目

在配置页面：

**Framework Preset**: Vite

**Root Directory**: `frontend`

**Build Command**: `npm run build`

**Output Directory**: `dist`

**Install Command**: `npm install`

#### 3. 配置环境变量

点击 "Environment Variables"，添加：

```bash
VITE_API_URL=https://your-backend-domain.railway.app/api/v1
```

**重要**：替换为你的 Railway 后端域名！

#### 4. 部署

1. 点击 "Deploy"
2. 等待部署完成（2-3分钟）
3. 部署成功后，会显示域名，例如：`sparkbox.vercel.app`

---

### 第六步：连接前后端（10分钟）

#### 1. 配置后端 CORS

Railway 后端需要允许 Vercel 域名访问。

编辑 `backend/main.py`，找到 CORS 配置：

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://sparkbox.vercel.app",  # 替换为你的 Vercel 域名
        "https://*.vercel.app",  # 允许所有 Vercel 预览域名
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

提交并推送：

```bash
cd d:\Cursor\sparkbox
git add backend/main.py
git commit -m "Update CORS for Vercel"
git push
```

Railway 会自动重新部署（1-2分钟）。

#### 2. 验证连接

1. 访问你的 Vercel 域名：`https://sparkbox.vercel.app`
2. 打开浏览器开发者工具（F12）
3. 查看 Console 和 Network 标签
4. 尝试注册/登录
5. 检查是否有 CORS 错误

---

### 第七步：测试功能（20分钟）

#### 1. 注册账号

1. 访问你的 Vercel 域名
2. 点击注册
3. 填写邮箱、密码、昵称
4. 提交注册

#### 2. 测试核心功能

- [ ] 登录
- [ ] 创建想法
- [ ] 查看想法列表
- [ ] 编辑想法
- [ ] 删除想法
- [ ] 创建分类
- [ ] 生成 AI 回顾
- [ ] 保存回顾
- [ ] 查看历史回顾
- [ ] 保存分享卡片

#### 3. 检查问题

如果遇到问题：

**前端无法访问后端**：
- 检查 Vercel 环境变量是否正确
- 检查 Railway 后端是否运行
- 检查 CORS 配置

**AI 生成失败**：
- 检查 Railway 环境变量中的 API Key
- 检查 API Key 是否有余额
- 查看 Railway 日志

**数据库错误**：
- Railway 会自动创建 SQLite 数据库
- 检查 Railway 日志

---

## 🎉 完成！

恭喜！你的 SparkBox 已经上线了！

### 访问地址

- **前端**：`https://your-project.vercel.app`
- **后端**：`https://your-backend.railway.app`
- **API 文档**：`https://your-backend.railway.app/docs`

### 分享给朋友

直接分享 Vercel 域名即可！

---

## 🔧 后续优化

### 1. 绑定自定义域名（可选）

**Vercel**：
1. 在 Vercel 项目设置中
2. Domains -> Add Domain
3. 输入你的域名
4. 按照提示配置 DNS

**Railway**：
1. 在 Railway 项目设置中
2. Domains -> Custom Domain
3. 输入你的域名
4. 配置 DNS

### 2. 配置数据库备份

Railway 的 SQLite 数据库会持久化，但建议定期备份：

1. 在 Railway 项目中
2. 点击 "Volumes"
3. 可以看到数据库文件
4. 定期下载备份

### 3. 监控和日志

**Railway 日志**：
- 在 Railway 项目中点击 "Deployments"
- 查看实时日志

**Vercel 日志**：
- 在 Vercel 项目中点击 "Deployments"
- 查看构建和运行日志

---

## 🐛 常见问题

### 1. 部署失败

**Railway 部署失败**：
- 检查 `requirements.txt` 是否正确
- 检查 `Procfile` 是否存在
- 查看部署日志

**Vercel 部署失败**：
- 检查 `package.json` 是否正确
- 检查构建命令是否正确
- 查看构建日志

### 2. CORS 错误

```javascript
// 确保后端 CORS 配置包含 Vercel 域名
allow_origins=[
    "https://your-project.vercel.app",
    "https://*.vercel.app",
]
```

### 3. 环境变量不生效

**Vercel**：
- 修改环境变量后需要重新部署
- Settings -> Environment Variables -> Redeploy

**Railway**：
- 修改环境变量后会自动重新部署

### 4. 数据库连接失败

Railway 的 SQLite 数据库路径：
```python
DATABASE_URL=sqlite:///./sparkbox.db
```

确保路径正确。

---

## 📊 成本说明

### 免费额度

**Vercel**：
- 带宽：100GB/月
- 构建时间：6000分钟/月
- 部署：无限次
- **足够个人使用**

**Railway**：
- $5 免费额度/月
- 约 500 小时运行时间
- **足够个人使用**

### 超出免费额度

**Vercel**：
- Pro 计划：$20/月
- 更多带宽和构建时间

**Railway**：
- 按使用量付费
- 约 $5-10/月

---

## 🎯 快速检查清单

部署前检查：
- [ ] `.gitignore` 文件已创建
- [ ] 前端 API 地址已修改
- [ ] 后端 `Procfile` 已创建
- [ ] `requirements.txt` 包含 gunicorn
- [ ] AI API Key 已准备

部署后检查：
- [ ] Railway 后端运行正常
- [ ] Vercel 前端访问正常
- [ ] 可以注册登录
- [ ] 可以创建想法
- [ ] 可以生成 AI 回顾

---

## 📞 需要帮助？

如果遇到问题：

1. **查看日志**
   - Railway: Deployments -> View Logs
   - Vercel: Deployments -> View Function Logs

2. **检查环境变量**
   - Railway: Variables 标签
   - Vercel: Settings -> Environment Variables

3. **重新部署**
   - Railway: Deployments -> Redeploy
   - Vercel: Deployments -> Redeploy

---

## 🎉 恭喜上线！

你的 SparkBox 现在已经在云端运行了！

**下一步**：
1. 分享给朋友试用
2. 收集反馈
3. 持续优化

**未来计划**：
1. 绑定自定义域名
2. 开发小程序版本
3. 开发 App 版本

---

**祝你使用愉快！** ✨

如有问题，随时查看文档或提问。
