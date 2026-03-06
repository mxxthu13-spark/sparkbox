# SparkBox 问题快速修复指南

## 已修复的问题

### ✅ 问题1：时间显示8小时前
**原因**：前端解析时间字符串时，`new Date()` 默认将不带时区的字符串当作 UTC 时间处理，导致中国时区（UTC+8）差了8小时。

**修复**：
- 文件：`frontend/src/components/ThoughtCard.vue`
- 方法：手动解析时间字符串，强制当作本地时间处理
- 状态：✅ 已修复

### ✅ 问题2：回顾统计与分类无关
**原因**：后端已支持分类筛选，但需要确保前端正确传递参数。

**修复**：
- 后端文件：`backend/api/thoughts.py` - 已支持 `category_ids` 参数
- 后端文件：`backend/api/ai.py` - AI 生成回顾时已应用分类筛选
- 前端文件：`frontend/src/pages/review/index.vue` - 已添加调试日志
- 状态：✅ 已修复

### ✅ 问题3：历史回顾详情页面显示乱码
**原因**：`detail.vue` 文件编码损坏，所有中文字符变成了 `????`。

**修复**：
- 文件：`frontend/src/pages/review/detail.vue`
- 方法：完全重建文件，使用 UTF-8 编码
- 状态：✅ 已修复

## 立即执行步骤

### 步骤1：重启后端（必须！）⚠️

后端代码已修改，必须重启才能生效：

```bash
# Windows PowerShell
cd d:\Cursor\sparkbox\backend

# 如果后端正在运行，按 Ctrl+C 停止

# 激活虚拟环境
.\venv\Scripts\activate

# 重新启动后端
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 步骤2：清除浏览器缓存（必须！）⚠️

前端代码已修改，必须清除缓存：

**方法1：强制刷新**
- 按 `Ctrl + Shift + R` 多次（推荐）

**方法2：清除缓存**
1. 按 `Ctrl + Shift + Delete`
2. 选择"缓存的图片和文件"
3. 点击"清除数据"

**方法3：清除 localStorage**
1. 按 `F12` 打开开发者工具
2. 在 Console 标签输入：`localStorage.clear()`
3. 按回车
4. 刷新页面

### 步骤3：测试时间显示

1. 创建一条新想法
2. 立即查看首页
3. 应该显示"刚刚"而不是"8小时前"

**如果还是显示8小时前**：
- 打开浏览器控制台（F12）
- 查看是否有红色错误信息
- 确认是否已清除缓存

### 步骤4：测试回顾统计

1. 打开回顾页面
2. 打开浏览器控制台（F12）
3. 选择时间范围（例如：最近30天）
4. 选择一个或多个分类
5. 查看控制台输出：
   ```
   查询想法数量，参数: {start_date: "2026-02-04", end_date: "2026-03-06", page: 1, page_size: 1, category_ids: "xxx,yyy"}
   查询结果: 共 X 条想法
   ```
6. 点击"✦ AI 生成回顾"
7. 查看控制台输出：
   ```
   生成回顾请求参数: {start_date: "...", end_date: "...", style: "insight", category_ids: [...]}
   生成回顾结果: {summary: "...", insight: "...", ...}
   ```
8. 确认统计数字与选择的分类匹配

### 步骤5：测试历史回顾详情

1. 生成一个新回顾并保存
2. 进入"历史回顾"列表
3. 点击一条回顾
4. 确认页面显示正常：
   - ✅ 标题显示正确（不是 `????`）
   - ✅ 统计信息显示正确（条想法、活跃天、个分类）
   - ✅ AI 内容显示正确
   - ✅ 原始想法列表显示正确
5. 点击"📤 查看分享卡片"
6. 确认卡片显示正常：
   - ✅ 标题"⚡ 闪念盒子"
   - ✅ 模式和主题
   - ✅ AI 生成的内容
   - ✅ 统计信息（条想法、活跃天、个分类）

## 验证清单

完成所有步骤后，逐一验证：

- [ ] 后端已重启（查看终端输出，应该有 "Application startup complete"）
- [ ] 浏览器缓存已清除（按 Ctrl+Shift+R 强制刷新）
- [ ] 新建想法显示"刚刚"（不是"8小时前"）
- [ ] 选择分类后，想法数量统计正确变化
- [ ] 生成回顾时，只包含选中分类的记录
- [ ] 历史回顾列表显示正常（有分类标签）
- [ ] 历史回顾详情页面显示正常（没有乱码）
- [ ] 分享卡片显示正常（有完整内容和统计）

## 调试技巧

### 查看后端日志

后端终端会显示所有 API 请求：

```
INFO:     127.0.0.1:xxxxx - "GET /api/v1/thoughts/?start_date=2026-02-04&end_date=2026-03-06&category_ids=xxx,yyy&page=1&page_size=1 HTTP/1.1" 200 OK
```

确认 URL 中包含 `category_ids` 参数。

### 查看前端日志

打开浏览器控制台（F12），查看 Console 标签：

```javascript
查询想法数量，参数: {start_date: "2026-02-04", end_date: "2026-03-06", page: 1, page_size: 1, category_ids: "xxx,yyy"}
查询结果: 共 5 条想法
生成回顾请求参数: {start_date: "2026-02-04", end_date: "2026-03-06", style: "insight", category_ids: ["xxx", "yyy"]}
生成回顾结果: {summary: "...", insight: "...", soul: "...", thought_count: 5, days: 3, categories: 2}
```

### 测试 API 接口

访问 http://localhost:8000/docs 测试 API：

1. 找到 `GET /api/v1/thoughts/` 接口
2. 点击 "Try it out"
3. 填写参数：
   - `start_date`: 2026-02-04
   - `end_date`: 2026-03-06
   - `category_ids`: 某个分类ID
4. 点击 "Execute"
5. 查看返回的 `total` 是否正确

## 常见问题

### Q1: 时间还是显示8小时前？

**解决方案**：
1. 确认已清除浏览器缓存（按 Ctrl+Shift+R）
2. 检查浏览器控制台是否有错误
3. 确认 `ThoughtCard.vue` 文件已更新

### Q2: 回顾统计还是显示所有记录？

**解决方案**：
1. 确认后端已重启
2. 打开浏览器控制台，查看请求参数是否包含 `category_ids`
3. 查看后端终端日志，确认收到了 `category_ids` 参数

### Q3: 历史回顾详情还是显示乱码？

**解决方案**：
1. 确认 `detail.vue` 文件已更新
2. 清除浏览器缓存
3. 检查文件编码是否为 UTF-8

### Q4: 分享卡片显示空白？

**解决方案**：
1. 打开浏览器控制台，查看是否有错误
2. 检查 localStorage：
   ```javascript
   console.log('卡片数据:', localStorage.getItem('shareCardData'))
   ```
3. 确认 `card.vue` 文件已更新

## 技术细节

### 时间解析修复

**修复前**：
```javascript
const d = new Date(ts) // 将 "2026-03-06 10:00:00" 当作 UTC 时间
```

**修复后**：
```javascript
// 手动解析为本地时间
const match = ts.match(/^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})/)
const d = new Date(
  parseInt(match[1]),      // year
  parseInt(match[2]) - 1,  // month (0-indexed)
  parseInt(match[3]),      // day
  parseInt(match[4]),      // hour
  parseInt(match[5]),      // minute
  parseInt(match[6])       // second
)
```

### 分类筛选修复

**后端**：
```python
# 支持多个分类ID，逗号分隔
if category_ids:
    cat_id_list = [cid.strip() for cid in category_ids.split(',') if cid.strip()]
    if cat_id_list:
        conditions.append(Thought.category_id.in_(cat_id_list))
```

**前端**：
```javascript
// 将分类ID数组转换为逗号分隔的字符串
if (selectedCategories.value.length > 0) {
  params.category_ids = selectedCategories.value.join(',')
}
```

## 需要帮助？

如果按照以上步骤操作后仍有问题，请提供：

1. **后端终端日志**：完整的启动日志和 API 请求日志
2. **浏览器控制台日志**：F12 → Console 标签的完整输出（包括错误）
3. **具体操作步骤**：你做了什么，期望看到什么，实际看到什么
4. **截图**：问题页面的截图

祝使用愉快！🎉
