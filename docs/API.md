# SparkBox API 文档 v1.0

## 基础信息

- **Base URL**: `http://localhost:8001/api/v1`
- **认证方式**: Bearer Token (JWT)
- **Content-Type**: `application/json`

## 认证接口

### 注册
```http
POST /auth/register
```

**请求体**:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "nickname": "用户昵称"
}
```

**响应**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "nickname": "用户昵称"
  }
}
```

### 登录
```http
POST /auth/login
```

**请求体**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**响应**: 同注册

## 想法接口

### 获取想法列表
```http
GET /thoughts/?page=1&page_size=20&category_ids=uuid1,uuid2&keyword=关键词
```

**查询参数**:
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20）
- `category_ids`: 分类ID列表（逗号分隔）
- `keyword`: 搜索关键词

**响应**:
```json
{
  "items": [
    {
      "id": "uuid",
      "content": "想法内容",
      "category_id": "uuid",
      "category": {
        "id": "uuid",
        "name": "分类名",
        "icon": "✨",
        "color": "#6366f1"
      },
      "tags": ["标签1", "标签2"],
      "mood": "happy",
      "ai_summary": "AI摘要",
      "ai_quote": "AI金句",
      "is_pinned": false,
      "created_at": "2024-03-06 10:30:00",
      "updated_at": "2024-03-06 10:30:00"
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 20
}
```

### 创建想法
```http
POST /thoughts/
```

**请求体**:
```json
{
  "content": "想法内容",
  "category_id": "uuid",
  "tags": ["标签1", "标签2"],
  "mood": "happy"
}
```

**响应**: 单个想法对象

### 获取想法详情
```http
GET /thoughts/{thought_id}
```

**响应**: 单个想法对象

### 更新想法
```http
PUT /thoughts/{thought_id}
```

**请求体**:
```json
{
  "content": "更新后的内容",
  "category_id": "uuid",
  "tags": ["新标签"],
  "is_pinned": true
}
```

**响应**: 更新后的想法对象

### 删除想法
```http
DELETE /thoughts/{thought_id}
```

**响应**:
```json
{
  "message": "删除成功"
}
```

## 分类接口

### 获取分类列表
```http
GET /categories/
```

**响应**:
```json
[
  {
    "id": "uuid",
    "name": "日常感悟",
    "icon": "✨",
    "color": "#6366f1",
    "created_at": "2024-03-06 10:30:00"
  }
]
```

### 创建分类
```http
POST /categories/
```

**请求体**:
```json
{
  "name": "新分类",
  "icon": "📝",
  "color": "#60a5fa"
}
```

**响应**: 单个分类对象

### 更新分类
```http
PUT /categories/{category_id}
```

**请求体**: 同创建分类

**响应**: 更新后的分类对象

### 删除分类
```http
DELETE /categories/{category_id}
```

**响应**:
```json
{
  "message": "删除成功"
}
```

## AI 接口

### 生成回顾
```http
POST /ai/generate-review
```

**请求体**:
```json
{
  "start_date": "2024-02-01",
  "end_date": "2024-03-06",
  "category_ids": ["uuid1", "uuid2"],
  "style": "insight"
}
```

**参数说明**:
- `style`: 回顾模式
  - `summary`: 摘要模式
  - `insight`: 洞察模式
  - `soul`: 灵魂模式

**响应**:
```json
{
  "summary": "摘要模式的内容...",
  "insight": "洞察模式的内容...",
  "soul": "灵魂模式的内容...",
  "theme": "长期主题",
  "thought_count": 10,
  "thoughts": [
    {
      "id": "uuid",
      "content": "想法内容",
      "created_at": "2024-03-06 10:30:00"
    }
  ]
}
```

## 回顾接口

### 获取回顾列表
```http
GET /reviews/?page=1&page_size=20
```

**响应**:
```json
{
  "items": [
    {
      "id": "uuid",
      "title": "回顾标题",
      "period_start": "2024-02-01",
      "period_end": "2024-03-06",
      "thought_count": 10,
      "thought_ids": ["uuid1", "uuid2"],
      "category_ids": ["uuid1", "uuid2"],
      "review_mode": "insight",
      "theme": "长期主题",
      "ai_content": "AI生成的内容...",
      "created_at": "2024-03-06 10:30:00"
    }
  ],
  "total": 5,
  "page": 1,
  "page_size": 20
}
```

### 创建回顾
```http
POST /reviews/
```

**请求体**:
```json
{
  "title": "回顾标题",
  "period_start": "2024-02-01",
  "period_end": "2024-03-06",
  "thought_count": 10,
  "thought_ids": ["uuid1", "uuid2"],
  "category_ids": ["uuid1", "uuid2"],
  "review_mode": "insight",
  "theme": "长期主题",
  "ai_content": "AI生成的内容..."
}
```

**响应**: 单个回顾对象

### 获取回顾详情
```http
GET /reviews/{review_id}
```

**响应**:
```json
{
  "id": "uuid",
  "title": "回顾标题",
  "period_start": "2024-02-01",
  "period_end": "2024-03-06",
  "thought_count": 10,
  "thought_ids": ["uuid1", "uuid2"],
  "category_ids": ["uuid1", "uuid2"],
  "review_mode": "insight",
  "theme": "长期主题",
  "ai_content": "AI生成的内容...",
  "created_at": "2024-03-06 10:30:00",
  "thoughts": [
    {
      "id": "uuid",
      "content": "想法内容",
      "created_at": "2024-03-06 10:30:00",
      "tags": ["标签1"]
    }
  ]
}
```

### 删除回顾
```http
DELETE /reviews/{review_id}
```

**响应**:
```json
{
  "message": "删除成功"
}
```

## 错误响应

所有接口在出错时返回统一格式：

```json
{
  "detail": "错误信息"
}
```

### 常见错误码

- `400`: 请求参数错误
- `401`: 未认证或 Token 过期
- `403`: 无权限访问
- `404`: 资源不存在
- `500`: 服务器内部错误

## 认证说明

除了注册和登录接口，其他所有接口都需要在请求头中携带 Token：

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 时间格式

- **日期**: `YYYY-MM-DD` (如: `2024-03-06`)
- **日期时间**: `YYYY-MM-DD HH:MM:SS` (如: `2024-03-06 10:30:00`)

## 分页说明

所有列表接口都支持分页，返回格式统一为：

```json
{
  "items": [],
  "total": 100,
  "page": 1,
  "page_size": 20
}
```

## 请求示例

### JavaScript (Fetch)
```javascript
const response = await fetch('http://localhost:8001/api/v1/thoughts/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
const data = await response.json()
```

### Python (requests)
```python
import requests

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.get(
    'http://localhost:8001/api/v1/thoughts/',
    headers=headers
)
data = response.json()
```

### cURL
```bash
curl -X GET "http://localhost:8001/api/v1/thoughts/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

## 速率限制

目前暂无速率限制，未来版本可能会添加。

## 版本历史

### v1.0 (2024-03-06)
- 初始版本发布
- 完整的想法管理功能
- AI 三种模式回顾
- 历史回顾管理
- 分类管理

---

更多信息请访问 [API 交互式文档](http://localhost:8001/docs)
