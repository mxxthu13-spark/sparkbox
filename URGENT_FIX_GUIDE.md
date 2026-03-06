# SparkBox 紧急修复指南

## 当前问题状态

### 问题1：时间显示8小时前 ⚠️
**状态**：已修复代码，需要测试
**文件**：`frontend/src/components/ThoughtCard.vue`
**修复**：手动解析时间字符串，避免时区问题

### 问题2：回顾统计与分类无关 ⚠️
**状态**：已修复代码，需要重启后端
**文件**：`backend/api/reviews.py`
**修复**：后端应用分类筛选

### 问题3：历史回顾卡片崩溃 ✅
**状态**：已修复
**文件**：`frontend/src/pages/review/card.vue`
**问题**：文件编码损坏，已重新创建

## 立即执行步骤

### 步骤1：重启后端（必须！）
```bash
# 停止当前后端进程（Ctrl+C）

# 重新启动
cd d:\Cursor\sparkbox\backend
venv\Scripts\activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 步骤2：清除浏览器缓存（必须！）
1. 打开浏览器
2. 按 `Ctrl+Shift+Delete`
3. 选择"缓存的图片和文件"
4. 点击"清除数据"
5. 或者直接按 `Ctrl+Shift+R` 强制刷新

### 步骤3：测试时间显示
1. 创建一条新想法
2. 立即查看首页
3. 应该显示"刚刚"而不是"8小时前"
4. 如果还是8小时前，打开浏览器控制台（F12）
5. 在Console中输入：
```javascript
const ts = "2026-03-05 22:35:26"
const parts = ts.split(/[T\-:.]/)
const d = new Date(
  parseInt(parts[0]),
  parseInt(parts[1]) - 1,
  parseInt(parts[2]),
  parseInt(parts[3]) || 0,
  parseInt(parts[4]) || 0,
  parseInt(parts[5]) || 0
)
console.log('解析时间:', d)
console.log('当前时间:', new Date())
console.log('时间差(小时):', (new Date() - d) / 3600000)
```

### 步骤4：测试回顾统计
1. 打开回顾页面
2. 打开浏览器控制台（F12）
3. 选择时间范围
4. 选择一个分类
5. 查看控制台输出：
   - "查询想法数量，参数: ..."
   - "查询结果: X"
6. 确认数字与选择的分类匹配

### 步骤5：测试分享卡片
1. 生成一个新回顾并保存
2. 进入历史回顾列表
3. 点击一条回顾
4. 点击"查看分享卡片"
5. 应该看到完整的卡片，包含：
   - 标题"⚡ 闪念盒子"
   - 模式和主题
   - AI生成的内容
   - 统计信息

## 如果问题仍然存在

### 时间显示问题
如果时间还是显示8小时前，可能是：
1. 浏览器缓存没清除 → 强制刷新
2. 后端返回的时间格式不对 → 检查后端日志
3. 系统时区设置问题 → 检查服务器时区

**临时解决方案**：
在 `ThoughtCard.vue` 中添加调试：
```javascript
function formatTime(ts) {
  console.log('原始时间:', ts)
  // ... 其他代码
  console.log('解析后:', d)
  console.log('当前时间:', now)
  console.log('时间差(毫秒):', diff)
  // ... 其他代码
}
```

### 回顾统计问题
如果统计还是不对，检查：
1. 后端是否重启 → 必须重启！
2. 前端是否传递了category_ids → 查看控制台日志
3. 后端是否收到参数 → 查看后端日志

**检查后端日志**：
在 `backend/api/thoughts.py` 的 `list_thoughts` 函数开头添加：
```python
print(f"查询参数: category_ids={category_ids}, start_date={start_date}, end_date={end_date}")
```

### 分享卡片问题
如果卡片还是空白：
1. 打开浏览器控制台
2. 查看是否有错误
3. 检查localStorage：
```javascript
console.log('卡片数据:', localStorage.getItem('shareCardData'))
```

## 数据库迁移（如果还没执行）

```bash
cd d:\Cursor\sparkbox\backend
python migrate_reviews.py
```

## 验证清单

- [ ] 后端已重启
- [ ] 浏览器缓存已清除
- [ ] 新建想法显示"刚刚"
- [ ] 选择分类后统计数字变化
- [ ] 生成回顾时只包含选中分类的记录
- [ ] 历史回顾详情显示正确的记录数
- [ ] 分享卡片正常显示
- [ ] 删除回顾功能正常

## 联系信息

如果以上步骤都执行了还有问题，请提供：
1. 浏览器控制台的完整错误信息
2. 后端终端的日志输出
3. 具体的操作步骤和预期结果
