# SparkBox 快速部署方案（PaaS 平台）

## 🚀 最简单的部署方式

如果你想快速上线，不想折腾服务器，推荐使用 PaaS 平台。

---

## 方案一：Vercel + Railway（推荐）

**优点**：
- ✅ 免费额度充足
- ✅ 自动 HTTPS
- ✅ 全球 CDN
- ✅ 自动部署
- ✅ 零配置

**成本**：免费（个人使用足够）

### 1. 部署前端到 Vercel

#### 步骤：

1. **注册 Vercel**
   - 访问 https://vercel.com
   - 使用 GitHub 账号登录

2. **上传代码到 GitHub**
   ```bash
   cd d:\Cursor\sparkbox
   git init
   git add frontend/
   git commit -m "Frontend code"
   git remote add origin https://github.com/yourusername/sparkbox-frontend.git
   git push -u origin main
   ```

3. **在 Vercel 导入项目**
   - 点击 "New Project"
   - 选择你的 GitHub 仓库
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **配置环境变量**
   - 在 Vercel 项目设置中添加：
   ```
   VITE_API_URL=https://your-backend-url.railway.app/api/v1
   ```

5. **修改前端代码**
   ```javascript
   // frontend/src/utils/api.js
   const BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'
   ```

6. **部署**
   - Vercel 会自动部署
   - 获得域名：`your-project.vercel.app`

### 2. 部署后端到 Railway

#### 步骤：

1. **注册 Railway**
   - 访问 https://railway.app
   - 使用 GitHub 账号登录

2. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的后端仓库

3. **配置环境变量**
   ```
   DATABASE_URL=sqlite:///./sparkbox.db
   SECRET_KEY=your-secret-key-here
   DEEPSEEK_API_KEY=your-api-key
   DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
   DEEPSEEK_MODEL=deepseek-chat
   PORT=8001
   ```

4. **创建 Procfile**
   ```
   web: gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
   ```

5. **部署**
   - Railway 会自动部署
   - 获得域名：`your-project.railway.app`

---

## 方案二：Render（一站式部署）

**优点**：
- ✅ 前后端一起部署
- ✅ 免费额度
- ✅ 自动 HTTPS
- ✅ 简单易用

**成本**：免费（有限制）

---

## 📊 方案对比

| 平台 | 前端 | 后端 | 数据库 | 成本 | 难度 |
|------|------|------|--------|------|------|
| Vercel + Railway | ✅ | ✅ | SQLite | 免费 | ⭐⭐ |
| Render | ✅ | ✅ | SQLite | 免费 | ⭐⭐ |
| 云服务器 | ✅ | ✅ | SQLite | ¥99/年 | ⭐⭐⭐ |

---

## 🎯 我的推荐

### 个人使用（免费）
**Vercel + Railway**
- 前端：Vercel（全球 CDN，速度快）
- 后端：Railway（免费额度充足）
- 数据库：SQLite（Railway 自带持久化存储）

### 国内用户
**阿里云/腾讯云服务器**
- 访问速度快
- 完全控制
- 成本：¥99/年

### 长期运营
**云服务器**
- 完全控制
- 性能稳定
- 成本可控

---

**祝部署顺利！** 🚀
