# SparkBox v1.0

> 一个优雅的思想记录与 AI 回顾工具

## 📖 项目简介

SparkBox（闪念盒子）是一个帮助用户记录日常想法、并通过 AI 进行深度回顾的应用。它不仅是一个笔记工具，更是一个思想沉淀和自我认知的助手。

### 核心特性

- 💡 **快速记录**：随时捕捉灵感和想法
- 🏷️ **分类管理**：多维度组织你的思考
- 🤖 **AI 回顾**：三种模式深度分析你的思想轨迹
- 📊 **时间筛选**：按时间范围回顾思考历程
- 🎨 **精美卡片**：生成可分享的回顾卡片
- 📱 **响应式设计**：适配各种设备

## 🎯 核心功能

### 1. 想法管理
- 创建、编辑、删除想法
- 按分类筛选
- 关键词搜索
- 标签管理
- 置顶功能

### 2. AI 回顾（三种模式）

#### 摘要模式
提炼最近一段时间最核心的思考方向，150-200字，分段清晰。

#### 洞察模式
指出想法背后的思想结构或价值观，挖掘深层次的思维模式。

#### 灵魂模式
像一段人与自己对话的文字，帮助看见更深层的意义，有温度、有共鸣。

### 3. 历史回顾
- 查看所有保存的回顾
- 显示时间范围、记录数、分类信息
- 查看完整 AI 内容和原始想法
- 删除回顾

### 4. 分享功能
- 生成精美的回顾卡片
- 保存为图片
- 统一的品牌设计

## 🏗️ 技术架构

### 后端
- **框架**：FastAPI
- **数据库**：SQLite + SQLAlchemy
- **AI 服务**：DeepSeek / Qwen
- **认证**：JWT Token
- **端口**：8001

### 前端
- **框架**：Vue 3 + Vite
- **状态管理**：Pinia
- **路由**：Vue Router
- **UI**：自定义设计
- **图片生成**：html2canvas
- **端口**：5173

### 数据库设计

#### thoughts 表
```sql
- id: UUID
- user_id: String
- content: Text
- category_id: UUID
- tags: JSON
- mood: String
- ai_summary: Text
- ai_quote: Text
- is_pinned: Boolean
- created_at: DateTime
- updated_at: DateTime
```

#### reviews 表
```sql
- id: UUID
- user_id: String
- title: String
- period_start: Date
- period_end: Date
- thought_count: Integer
- thought_ids: JSON
- category_ids: JSON
- review_mode: String (summary/insight/soul)
- theme: String
- ai_content: Text
- created_at: DateTime
```

#### categories 表
```sql
- id: UUID
- user_id: String
- name: String
- icon: String
- color: String
- created_at: DateTime
```

## 🎨 设计规范

### Logo
- **图标**：层叠方块（代表思想的积累和沉淀）
- **颜色**：#6366f1（品牌紫色）
- **位置**：首页、回顾卡片、分享卡片

### 配色方案
```css
主色：#6366f1 (品牌紫)
辅助色：
  - 摘要模式：#f87171 (红)
  - 洞察模式：#60a5fa (蓝)
  - 灵魂模式：#a78bfa (紫)
背景色：#f8f8fa
文字色：#111827 / #374151 / #6b7280
```

### 字体
- 标题：700 weight
- 正文：400 weight
- 标签：500 weight

## 📦 项目结构

```
sparkbox/
├── backend/                 # 后端代码
│   ├── api/                # API 路由
│   │   ├── auth.py        # 认证相关
│   │   ├── thoughts.py    # 想法管理
│   │   ├── reviews.py     # 回顾管理
│   │   ├── categories.py  # 分类管理
│   │   └── ai.py          # AI 服务
│   ├── core/              # 核心配置
│   │   ├── config.py      # 配置文件
│   │   ├── database.py    # 数据库连接
│   │   └── security.py    # 安全相关
│   ├── models/            # 数据模型
│   │   ├── user.py
│   │   ├── thought.py
│   │   ├── review.py
│   │   └── category.py
│   ├── services/          # 业务逻辑
│   │   └── ai/           # AI 服务
│   │       ├── base.py
│   │       ├── deepseek.py
│   │       └── qwen.py
│   ├── main.py           # 应用入口
│   └── requirements.txt  # 依赖列表
│
├── frontend/              # 前端代码
│   ├── src/
│   │   ├── assets/       # 静态资源
│   │   ├── components/   # 组件
│   │   │   ├── BottomNav.vue
│   │   │   └── ...
│   │   ├── pages/        # 页面
│   │   │   ├── home/     # 首页
│   │   │   ├── review/   # 回顾页面
│   │   │   ├── thought/  # 想法详情
│   │   │   └── ...
│   │   ├── store/        # 状态管理
│   │   │   └── thoughts.js
│   │   ├── utils/        # 工具函数
│   │   │   └── api.js
│   │   ├── App.vue       # 根组件
│   │   └── main.js       # 入口文件
│   ├── package.json
│   └── vite.config.js
│
└── docs/                  # 文档
    ├── README.md
    ├── API.md
    ├── DEPLOYMENT.md
    └── CHANGELOG.md
```

## 🚀 快速开始

### 环境要求
- Python 3.9+
- Node.js 16+
- SQLite 3

### 后端启动

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
# 复制 .env.example 为 .env
# 填写 DEEPSEEK_API_KEY 或 QWEN_API_KEY

# 启动服务
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 访问应用
- 前端：http://localhost:5173
- 后端 API：http://localhost:8001
- API 文档：http://localhost:8001/docs

## 📝 使用指南

### 1. 注册/登录
首次使用需要注册账号，之后使用邮箱和密码登录。

### 2. 记录想法
1. 点击首页的"+"按钮
2. 输入想法内容
3. 选择分类（可选）
4. 添加标签（可选）
5. 点击保存

### 3. 生成 AI 回顾
1. 进入"回顾"页面
2. 选择时间范围（默认最近30天）
3. 选择分类（可多选，可不选）
4. 查看记录数量
5. 点击"✦ AI 生成回顾"
6. 切换三种模式查看不同角度的洞察
7. 点击"保存回顾"保存到历史

### 4. 查看历史回顾
1. 在回顾页面向下滚动
2. 查看"📚 历史回顾"列表
3. 点击任意回顾查看详情
4. 查看 AI 内容、原始想法、分类信息

### 5. 分享回顾
1. 生成回顾后
2. 点击"保存图片"
3. 图片自动下载到本地

## 🔧 配置说明

### 后端配置 (.env)
```env
# 数据库
DATABASE_URL=sqlite:///./sparkbox.db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI 服务（二选一）
DEEPSEEK_API_KEY=your-deepseek-api-key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat

# 或
QWEN_API_KEY=your-qwen-api-key
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-plus
```

### 前端配置
API 地址在 `frontend/src/utils/api.js` 中配置：
```javascript
const BASE_URL = 'http://localhost:8001/api/v1'
```

## 🐛 常见问题

### 1. 时间显示不正确
确保后端返回的时间格式为 `YYYY-MM-DD HH:MM:SS`，前端会自动解析为本地时间。

### 2. DELETE 请求失败
确保前端 API 请求中，DELETE 方法不传递 `data` 参数。

### 3. AI 生成失败
检查 AI API Key 是否正确配置，网络是否正常。

### 4. 浏览器缓存问题
修改代码后，按 `Ctrl+Shift+R` 强制刷新浏览器缓存。

### 5. 后端端口占用
如果 8000 端口被占用，可以使用 8001 端口，并修改前端 API 地址。

## 📊 性能优化

### 后端
- 使用异步数据库操作
- 合理的索引设计
- API 响应缓存

### 前端
- 组件懒加载
- 图片懒加载
- 防抖和节流
- 虚拟滚动（大列表）

## 🔒 安全性

- JWT Token 认证
- 密码加密存储
- SQL 注入防护
- XSS 防护
- CORS 配置

## 🚢 部署指南

### Docker 部署（推荐）
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

### 传统部署
参考 `docs/DEPLOYMENT.md`

## 📈 未来规划

### v1.1
- [ ] 数据导出功能
- [ ] 更多 AI 模型支持
- [ ] 移动端适配优化
- [ ] 暗黑模式

### v2.0
- [ ] 多人协作
- [ ] 想法关联图谱
- [ ] 语音输入
- [ ] 图片附件支持

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 开源协议

MIT License

## 👥 作者

SparkBox Team

## 🙏 致谢

感谢所有使用和支持 SparkBox 的用户！

---

**SparkBox v1.0** - 让思想沉淀，让洞察涌现 ✨
