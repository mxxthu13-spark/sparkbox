# 🚀 SparkBox 专属部署教程（mxxthu13-spark）

## 📝 你的信息

- GitHub 用户名：`mxxthu13-spark`
- DeepSeek API Key：`sk-730f3f4790f64c98b2c7593d2b0da191`

---

## 第一步：上传代码到 GitHub（15分钟）

### 1. 打开命令提示符（CMD）

**方法1**：
- 按键盘上的 `Win + R`
- 输入 `cmd`
- 按回车

**方法2**：
- 点击开始菜单
- 搜索"命令提示符"或"cmd"
- 点击打开

### 2. 进入项目目录

在命令提示符中，**复制粘贴**这行命令，然后按回车：

```bash
cd d:\Cursor\sparkbox
```

### 3. 配置 Git（只需要做一次）

**复制粘贴**下面两行命令（一行一行来）：

```bash
git config --global user.name "mxxthu13-spark"
```

按回车，然后：

```bash
git config --global user.email "your-email@example.com"
```

**注意**：把 `your-email@example.com` 改成你注册 GitHub 时用的邮箱

### 4. 初始化 Git 仓库

**复制粘贴**这行命令：

```bash
git init
```

### 5. 添加所有文件

**复制粘贴**这行命令：

```bash
git add .
```

### 6. 提交代码

**复制粘贴**这行命令：

```bash
git commit -m "SparkBox v1.0 - Initial commit"
```

### 7. 在 GitHub 创建仓库

1. 打开浏览器，访问：https://github.com/new
2. 在 "Repository name" 填入：`sparkbox`
3. 选择 "Public"（公开）
4. **不要勾选**任何初始化选项
5. 点击绿色按钮 "Create repository"

### 8. 推送代码到 GitHub

**复制粘贴**这两行命令（一行一行来）：

```bash
git remote add origin https://github.com/mxxthu13-spark/sparkbox.git
```

按回车，然后：

```bash
git branch -M main
```

按回车，然后：

```bash
git push -u origin main
```

**如果要求输入用户名和密码**：
- 用户名：`mxxthu13-spark`
- 密码：需要使用 Personal Access Token（不是你的 GitHub 密码）

**如何获取 Token**：
1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" -> "Generate new token (classic)"
3. Note 填：`sparkbox`
4. 勾选 `repo` 权限
5. 点击底部 "Generate token"
6. **复制这个 token**（只显示一次！）
7. 在命令行输入密码时，粘贴这个 token

---

## 第二步：部署后端到 Railway（20分钟）

### 1. 登录 Railway

1. 打开：https://railway.app/dashboard
2. 用你的 GitHub 账号登录

### 2. 创建新项目

1. 点击右上角紫色按钮 "New Project"
2. 选择 "Deploy from GitHub repo"
3. 如果提示授权，点击 "Configure GitHub App"
4. 选择 "Only select repositories"
5. 选择 `sparkbox` 仓库
6. 点击 "Install & Authorize"
7. 回到 Railway，选择 `sparkbox` 仓库

### 3. 配置项目

1. 项目创建后，点击项目卡片
2. 点击 "Settings" 标签
3. 找到 "Root Directory"
4. 填入：`backend`
5. 点击外面保存

### 4. 添加环境变量

1. 点击 "Variables" 标签
2. 点击 "New Variable"
3. **一个一个添加**下面的变量：

**变量1**：
- Variable：`DATABASE_URL`
- Value：`sqlite:///./sparkbox.db`

**变量2**：
- Variable：`SECRET_KEY`
- Value：`a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6`

**变量3**：
- Variable：`DEEPSEEK_API_KEY`
- Value：`sk-730f3f4790f64c98b2c7593d2b0da191`

**变量4**：
- Variable：`DEEPSEEK_BASE_URL`
- Value：`https://api.deepseek.com/v1`

**变量5**：
- Variable：`DEEPSEEK_MODEL`
- Value：`deepseek-chat`

**变量6**：
- Variable：`PORT`
- Value：`8001`

### 5. 部署

1. 点击 "Deployments" 标签
2. Railway 会自动开始部署
3. 等待 3-5 分钟
4. 看到 "Success" 就成功了

### 6. 获取域名

1. 点击 "Settings" 标签
2. 找到 "Domains" 部分
3. 点击 "Generate Domain"
4. 会生成一个域名，例如：`sparkbox-production-xxxx.up.railway.app`
5. **复制这个域名**，保存到记事本

### 7. 测试后端

在浏览器访问：`https://你的域名.railway.app/docs`

应该能看到 API 文档页面。

---

## 第三步：部署前端到 Vercel（15分钟）

### 1. 登录 Vercel

1. 打开：https://vercel.com/dashboard
2. 用你的账号登录

### 2. 导入项目

1. 点击右上角 "Add New..." 按钮
2. 选择 "Project"
3. 找到 `sparkbox` 仓库
4. 点击 "Import"

### 3. 配置项目

在配置页面填写：

**Framework Preset**：选择 `Vite`

**Root Directory**：点击 "Edit"，填入 `frontend`

**Build Command**：`npm run build`

**Output Directory**：`dist`

**Install Command**：`npm install`

### 4. 添加环境变量

1. 展开 "Environment Variables"
2. 添加一个变量：
   - Name：`VITE_API_URL`
   - Value：`https://你的Railway域名.railway.app/api/v1`
   
   **重要**：把 `你的Railway域名` 替换成第二步第6点复制的域名！
   
   例如：`https://sparkbox-production-xxxx.up.railway.app/api/v1`

### 5. 部署

1. 点击底部蓝色按钮 "Deploy"
2. 等待 2-3 分钟
3. 看到庆祝动画就成功了！

### 6. 获取你的网站地址

部署成功后，会显示你的网站地址，例如：
```
https://sparkbox-mxxthu13-spark.vercel.app
```

**复制这个地址**，这就是你的网站！

---

## 第四步：测试网站（10分钟）

### 1. 访问你的网站

在浏览器打开你的 Vercel 地址

### 2. 注册账号

1. 点击"注册"
2. 填写邮箱、密码、昵称
3. 点击注册

### 3. 测试功能

- 创建一个想法
- 查看想法列表
- 生成 AI 回顾
- 保存回顾

### 4. 如果遇到问题

**问题1：无法连接后端**
- 检查 Vercel 的环境变量是否正确
- 确认 Railway 后端是否运行

**问题2：AI 生成失败**
- 检查 DeepSeek API Key 是否正确
- 检查 API Key 是否有余额

---

## 🎉 完成！

恭喜！你的 SparkBox 已经上线了！

### 你的网站信息

- **前端地址**：`https://sparkbox-mxxthu13-spark.vercel.app`
- **后端地址**：`https://你的Railway域名.railway.app`
- **API 文档**：`https://你的Railway域名.railway.app/docs`

### 分享给朋友

直接把前端地址发给朋友就可以了！

---

## 📞 如果遇到问题

### 查看日志

**Railway 日志**：
1. 打开 Railway 项目
2. 点击 "Deployments"
3. 点击最新的部署
4. 查看日志

**Vercel 日志**：
1. 打开 Vercel 项目
2. 点击 "Deployments"
3. 点击最新的部署
4. 查看日志

### 常见问题

**Q: Git 推送失败**
- 确认已经创建了 Personal Access Token
- 确认 token 有 repo 权限

**Q: Railway 部署失败**
- 检查环境变量是否都添加了
- 查看部署日志

**Q: Vercel 无法访问后端**
- 检查 `VITE_API_URL` 环境变量
- 确认末尾有 `/api/v1`

---

## 💡 提示

- 所有命令都可以直接复制粘贴
- 遇到问题可以截图给我看
- 每一步都不要跳过

---

**准备好了吗？从第一步开始吧！** 🚀

有任何问题随时告诉我！
