# SparkBox 微信小程序部署方案

## 📱 概述

将 SparkBox 部署为微信小程序，让用户可以在微信中直接使用。

---

## 🎯 架构说明

### 当前架构
```
前端（Vue 3 + Vite）
    ↓
后端（FastAPI）
    ↓
数据库（SQLite）
```

### 小程序架构
```
小程序前端（原生/uni-app）
    ↓
后端（FastAPI）- 需要备案域名和 HTTPS
    ↓
数据库（SQLite/MySQL）
```

---

## 🔄 两种方案

### 方案一：使用 uni-app 改造（推荐）

**优点**：
- ✅ 代码复用率高（70%+）
- ✅ 一次开发，多端发布
- ✅ Vue 3 语法相似
- ✅ 开发效率高

**缺点**：
- ⚠️ 需要改造现有代码
- ⚠️ 部分 API 需要适配

### 方案二：原生小程序开发

**优点**：
- ✅ 性能最优
- ✅ 功能完整
- ✅ 官方支持

**缺点**：
- ⚠️ 需要重写前端
- ⚠️ 开发周期长
- ⚠️ 维护成本高

---

## 🚀 方案一：uni-app 改造（详细步骤）

### 第一步：准备工作

#### 1. 注册微信小程序

1. **访问微信公众平台**
   - https://mp.weixin.qq.com/
   - 注册小程序账号（个人/企业）

2. **获取 AppID**
   - 登录小程序后台
   - 开发 -> 开发设置
   - 复制 AppID

3. **配置服务器域名**
   - 开发 -> 开发设置 -> 服务器域名
   - request 合法域名：`https://your-domain.com`
   - uploadFile 合法域名：`https://your-domain.com`
   - downloadFile 合法域名：`https://your-domain.com`
   
   **注意**：
   - 必须是 HTTPS
   - 必须备案（国内服务器）
   - 不能是 IP 地址

#### 2. 安装开发工具

```bash
# 安装 HBuilderX（uni-app 官方 IDE）
# 下载地址：https://www.dcloud.io/hbuilderx.html

# 或使用 VS Code + uni-app 插件
# 安装 uni-app 插件
```

#### 3. 安装微信开发者工具

```bash
# 下载地址：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html
```

### 第二步：创建 uni-app 项目

#### 1. 使用 HBuilderX 创建

1. 文件 -> 新建 -> 项目
2. 选择 uni-app
3. 模板选择：默认模板
4. 项目名称：sparkbox-miniapp

#### 2. 或使用 Vue CLI 创建

```bash
# 安装 Vue CLI
npm install -g @vue/cli

# 创建 uni-app 项目
vue create -p dcloudio/uni-preset-vue sparkbox-miniapp

# 选择 Vue 3 模板
```

### 第三步：迁移代码

#### 1. 项目结构对比

**现有 Vue 3 项目**：
```
frontend/src/
├── assets/
├── components/
├── pages/
├── store/
├── utils/
├── App.vue
└── main.js
```

**uni-app 项目**：
```
sparkbox-miniapp/
├── pages/           # 页面
├── components/      # 组件
├── static/          # 静态资源
├── store/           # 状态管理
├── utils/           # 工具函数
├── App.vue          # 应用配置
├── main.js          # 入口文件
├── manifest.json    # 应用配置
└── pages.json       # 页面配置
```

#### 2. 配置 pages.json

```json
{
  "pages": [
    {
      "path": "pages/home/index",
      "style": {
        "navigationBarTitleText": "闪念盒子"
      }
    },
    {
      "path": "pages/review/index",
      "style": {
        "navigationBarTitleText": "AI 回顾"
      }
    },
    {
      "path": "pages/review/history",
      "style": {
        "navigationBarTitleText": "历史回顾"
      }
    },
    {
      "path": "pages/review/detail",
      "style": {
        "navigationBarTitleText": "回顾详情"
      }
    },
    {
      "path": "pages/thought/detail",
      "style": {
        "navigationBarTitleText": "想法详情"
      }
    }
  ],
  "globalStyle": {
    "navigationBarTextStyle": "black",
    "navigationBarTitleText": "闪念盒子",
    "navigationBarBackgroundColor": "#FFFFFF",
    "backgroundColor": "#F8F8FA"
  },
  "tabBar": {
    "color": "#999999",
    "selectedColor": "#6366F1",
    "backgroundColor": "#FFFFFF",
    "list": [
      {
        "pagePath": "pages/home/index",
        "iconPath": "static/tabbar/home.png",
        "selectedIconPath": "static/tabbar/home-active.png",
        "text": "首页"
      },
      {
        "pagePath": "pages/review/index",
        "iconPath": "static/tabbar/review.png",
        "selectedIconPath": "static/tabbar/review-active.png",
        "text": "回顾"
      }
    ]
  }
}
```

#### 3. 配置 manifest.json

```json
{
  "name": "闪念盒子",
  "appid": "你的微信小程序AppID",
  "description": "思想记录与 AI 回顾工具",
  "versionName": "1.0.0",
  "versionCode": "100",
  "mp-weixin": {
    "appid": "你的微信小程序AppID",
    "setting": {
      "urlCheck": true,
      "es6": true,
      "postcss": true,
      "minified": true
    },
    "usingComponents": true,
    "permission": {
      "scope.userLocation": {
        "desc": "用于记录想法时的位置信息"
      }
    }
  }
}
```

#### 4. 修改 API 请求

**原有代码**（frontend/src/utils/api.js）：
```javascript
const BASE_URL = 'http://localhost:8001/api/v1'

export function request(method, url, data = null) {
  const config = {
    method,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : ''
    }
  }
  
  if (method !== 'DELETE' && data !== null) {
    config.body = JSON.stringify(data)
  }
  
  return fetch(BASE_URL + url, config)
}
```

**uni-app 代码**（utils/api.js）：
```javascript
const BASE_URL = 'https://your-domain.com/api/v1'

export function request(method, url, data = null) {
  const token = uni.getStorageSync('access_token')
  
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + url,
      method: method,
      data: method !== 'DELETE' ? data : undefined,
      header: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else {
          reject(res.data)
        }
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

// API 封装
export const api = {
  // 认证
  auth: {
    login: (data) => request('POST', '/auth/login', data),
    register: (data) => request('POST', '/auth/register', data)
  },
  
  // 想法
  thoughts: {
    list: (params) => request('GET', `/thoughts/?${new URLSearchParams(params)}`),
    get: (id) => request('GET', `/thoughts/${id}`),
    create: (data) => request('POST', '/thoughts/', data),
    update: (id, data) => request('PUT', `/thoughts/${id}`, data),
    delete: (id) => request('DELETE', `/thoughts/${id}`)
  },
  
  // 回顾
  reviews: {
    list: (params) => request('GET', `/reviews/?${new URLSearchParams(params)}`),
    get: (id) => request('GET', `/reviews/${id}`),
    create: (data) => request('POST', '/reviews/', data),
    delete: (id) => request('DELETE', `/reviews/${id}`)
  },
  
  // AI
  ai: {
    generateReview: (data) => request('POST', '/ai/generate-review', data)
  },
  
  // 分类
  categories: {
    list: () => request('GET', '/categories/'),
    create: (data) => request('POST', '/categories/', data),
    update: (id, data) => request('PUT', `/categories/${id}`, data),
    delete: (id) => request('DELETE', `/categories/${id}`)
  }
}
```

#### 5. 修改页面代码

**关键差异**：

| 功能 | Vue 3 | uni-app |
|------|-------|---------|
| 路由跳转 | `router.push()` | `uni.navigateTo()` |
| 本地存储 | `localStorage` | `uni.getStorageSync()` |
| 提示信息 | 自定义 | `uni.showToast()` |
| 网络请求 | `fetch` | `uni.request()` |
| 图片选择 | `<input type="file">` | `uni.chooseImage()` |

**示例改造**（首页）：

```vue
<template>
  <view class="page">
    <!-- 头部 -->
    <view class="header">
      <view class="logo-section">
        <image class="logo-icon" src="/static/logo.png" mode="aspectFit"></image>
        <text class="app-title">闪念盒子</text>
      </view>
      <view class="header-actions">
        <view class="search-btn" @click="showSearch = !showSearch">🔍</view>
        <view class="stats-badge" @click="goStats">
          <text>{{ total }}</text>
          <text class="stats-unit"> 条</text>
        </view>
      </view>
    </view>

    <!-- 想法列表 -->
    <scroll-view class="thoughts-list" scroll-y>
      <view 
        v-for="thought in thoughts" 
        :key="thought.id"
        class="thought-item"
        @click="openThought(thought.id)"
      >
        <view class="thought-header">
          <text class="thought-time">{{ formatTime(thought.created_at) }}</text>
          <text v-if="thought.category" class="thought-category">
            {{ thought.category.icon }} {{ thought.category.name }}
          </text>
        </view>
        <text class="thought-content">{{ thought.content }}</text>
      </view>
    </scroll-view>

    <!-- 添加按钮 -->
    <view class="add-btn" @click="addThought">
      <text>+</text>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/utils/api'

const thoughts = ref([])
const total = ref(0)
const showSearch = ref(false)

async function loadThoughts() {
  try {
    uni.showLoading({ title: '加载中...' })
    const res = await api.thoughts.list({ page: 1, page_size: 20 })
    thoughts.value = res.items
    total.value = res.total
    uni.hideLoading()
  } catch (e) {
    uni.hideLoading()
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
}

function openThought(id) {
  uni.navigateTo({
    url: `/pages/thought/detail?id=${id}`
  })
}

function addThought() {
  uni.navigateTo({
    url: '/pages/thought/create'
  })
}

function formatTime(time) {
  // 时间格式化逻辑
  const now = new Date()
  const created = new Date(time)
  const diff = (now - created) / 1000
  
  if (diff < 60) return '刚刚'
  if (diff < 3600) return `${Math.floor(diff / 60)}分钟前`
  if (diff < 86400) return `${Math.floor(diff / 3600)}小时前`
  return `${Math.floor(diff / 86400)}天前`
}

onMounted(() => {
  loadThoughts()
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #f8f8fa;
}

.header {
  background: #fff;
  padding: 20rpx 32rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.logo-icon {
  width: 64rpx;
  height: 64rpx;
}

.app-title {
  font-size: 48rpx;
  font-weight: 700;
  color: #111827;
}

.thoughts-list {
  height: calc(100vh - 200rpx);
  padding: 32rpx;
}

.thought-item {
  background: #fff;
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;
}

.thought-content {
  font-size: 28rpx;
  line-height: 1.6;
  color: #374151;
}

.add-btn {
  position: fixed;
  right: 32rpx;
  bottom: 120rpx;
  width: 112rpx;
  height: 112rpx;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 32rpx rgba(99, 102, 241, 0.3);
  
  text {
    font-size: 64rpx;
    color: #fff;
    font-weight: 300;
  }
}
</style>
```

### 第四步：后端适配

#### 1. 配置 CORS

```python
# backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-domain.com",
        "https://servicewechat.com",  # 微信小程序域名
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 2. 部署后端到有备案域名的服务器

**必须满足**：
- ✅ HTTPS（SSL 证书）
- ✅ 备案域名（国内服务器必须）
- ✅ 在小程序后台配置服务器域名

### 第五步：测试和发布

#### 1. 本地测试

```bash
# 在 HBuilderX 中
# 运行 -> 运行到小程序模拟器 -> 微信开发者工具

# 或使用命令行
npm run dev:mp-weixin
```

#### 2. 真机测试

1. 在微信开发者工具中点击"预览"
2. 扫描二维码
3. 在手机上测试

#### 3. 提交审核

1. 在微信开发者工具中点击"上传"
2. 填写版本号和备注
3. 登录小程序后台
4. 版本管理 -> 开发版本 -> 提交审核
5. 填写审核信息
6. 等待审核（1-7天）

#### 4. 发布上线

审核通过后：
1. 版本管理 -> 审核版本 -> 发布
2. 用户即可搜索使用

---

## 📋 关键注意事项

### 1. 域名要求

**必须**：
- ✅ HTTPS（443端口）
- ✅ 备案（国内服务器）
- ✅ 不能是 IP 地址
- ✅ 不能是 localhost

**推荐配置**：
```
前端：小程序
后端：阿里云/腾讯云服务器 + 备案域名
数据库：MySQL（推荐）或 SQLite
```

### 2. 小程序限制

**包大小**：
- 主包：≤ 2MB
- 分包：每个 ≤ 2MB
- 总大小：≤ 20MB

**网络请求**：
- 并发限制：10个
- 超时时间：60秒
- 必须 HTTPS

**本地存储**：
- 限制：10MB
- 使用 `uni.setStorageSync()`

### 3. 功能限制

**不支持**：
- ❌ `<iframe>`
- ❌ `document.cookie`
- ❌ `window.location`
- ❌ `eval()`

**需要适配**：
- 图片上传
- 文件下载
- 分享功能
- 支付功能

---

## 💰 成本估算

### 开发成本
- uni-app 改造：2-3周
- 测试调试：1周
- 审核发布：1周
- **总计**：4-5周

### 运营成本
- 服务器：¥99-200/年
- 域名：¥30-60/年
- 备案：免费
- 小程序认证：¥300/年（企业）或 免费（个人）
- **总计**：¥129-560/年

---

## 🎯 快速开始

### 最小可行方案（MVP）

1. **注册小程序**（1天）
   - 个人小程序（免费）
   - 获取 AppID

2. **购买服务器和域名**（1天）
   - 阿里云服务器：¥99/年
   - 域名：¥30/年
   - 备案：15-20天

3. **部署后端**（1天）
   - 参考 `docs/CLOUD_DEPLOYMENT.md`
   - 配置 HTTPS
   - 配置 CORS

4. **改造前端**（1-2周）
   - 创建 uni-app 项目
   - 迁移核心功能
   - 适配小程序 API

5. **测试发布**（1周）
   - 本地测试
   - 真机测试
   - 提交审核

---

## 📞 需要帮助？

### 官方文档
- uni-app：https://uniapp.dcloud.net.cn/
- 微信小程序：https://developers.weixin.qq.com/miniprogram/dev/framework/

### 常见问题

**Q: 必须要备案吗？**  
A: 是的，使用国内服务器必须备案。或者使用香港/国外服务器（不需要备案，但速度慢）。

**Q: 个人可以注册小程序吗？**  
A: 可以，但功能有限制（如不能开通支付）。

**Q: 改造工作量大吗？**  
A: 使用 uni-app，代码复用率可达 70%+，主要是 API 适配工作。

**Q: 可以同时支持 H5 和小程序吗？**  
A: 可以！uni-app 一次开发，多端发布。

---

## 🎉 总结

将 SparkBox 改造为微信小程序：

**优点**：
- ✅ 用户触达更广
- ✅ 微信生态内使用方便
- ✅ 可以使用微信登录

**挑战**：
- ⚠️ 需要备案域名
- ⚠️ 需要改造前端代码
- ⚠️ 审核周期较长

**建议**：
1. 先部署 Web 版本（Vercel + Railway）
2. 积累用户和反馈
3. 再考虑小程序版本

---

**祝开发顺利！** 🚀
