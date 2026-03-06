# SparkBox 完整修复步骤

## 第一步：运行数据库迁移（必须！）

```bash
cd d:\Cursor\sparkbox\backend
python migrate_reviews.py
```

**预期输出**：
```
开始数据库迁移...
✓ category_ids 字段已添加/已存在
✓ theme 字段已添加/已存在
✓ review_mode 字段已添加/已存在
✓ ai_content 字段已添加/已存在
数据库迁移完成！
```

## 第二步：测试数据库

```bash
cd d:\Cursor\sparkbox\backend
python test_reviews.py
```

查看输出，确认：
- reviews 表有 category_ids, theme, review_mode, ai_content 字段
- 能看到想法记录和分类统计

## 第三步：重启后端（必须！）

**停止当前后端**：
- 找到运行后端的终端窗口
- 按 `Ctrl+C` 停止

**重新启动**：
```bash
cd d:\Cursor\sparkbox\backend
venv\Scripts\activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**确认启动成功**：
看到类似输出：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

## 第四步：测试后端API

打开浏览器访问：
```
http://localhost:8000/docs
```

测试以下接口：
1. `GET /api/v1/thoughts/` - 添加参数 `category_ids=某个分类ID`
2. 查看返回的 `total` 是否正确

## 第五步：清除前端缓存

### 方法1：硬刷新
1. 打开前端页面
2. 按 `Ctrl+Shift+R` （Windows）或 `Cmd+Shift+R` （Mac）
3. 多按几次确保刷新

### 方法2：清除所有缓存
1. 按 `F12` 打开开发者工具
2. 右键点击刷新按钮
3. 选择"清空缓存并硬性重新加载"

### 方法3：清除localStorage
1. 按 `F12` 打开开发者工具
2. 切换到 Console 标签
3. 输入并回车：
```javascript
localStorage.clear()
location.reload()
```

## 第六步：测试时间显示

1. 创建一条新想法
2. 立即查看首页
3. **应该显示"刚刚"**

**如果还是显示"8小时前"**：
1. 按 `F12` 打开控制台
2. 在 Console 中输入：
```javascript
// 测试时间解析
const testTime = "2026-03-05 22:35:26"
const match = testTime.match(/^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})/)
const d = new Date(
  parseInt(match[1]),
  parseInt(match[2]) - 1,
  parseInt(match[3]),
  parseInt(match[4]),
  parseInt(match[5]),
  parseInt(match[6])
)
console.log('解析时间:', d)
console.log('当前时间:', new Date())
console.log('时间差(小时):', (new Date() - d) / 3600000)
```

## 第七步：测试回顾统计

1. 打开回顾页面
2. 按 `F12` 打开控制台
3. 选择时间范围（如最近30天）
4. **不选择任何分类**，查看"找到X条想法记录"
5. **选择一个分类**，查看数字是否变化
6. 在控制台查看日志：
   - "查询想法数量，参数: ..."
   - "查询结果: X"

**如果数字不变化**：
- 检查控制台是否有错误
- 检查 Network 标签，查看 `/api/v1/thoughts/` 请求
- 确认请求参数中有 `category_ids`

## 第八步：测试生成和保存回顾

1. 选择时间范围
2. **选择1-2个分类**（重要！）
3. 点击"AI 生成回顾"
4. 等待生成完成
5. 点击"保存回顾"
6. 进入"历史回顾"页面

**检查历史记录**：
- 应该显示时间范围
- 应该显示选择的分类标签
- 应该显示回顾模式
- 应该显示主题
- 想法数量应该是选中分类的数量，不是全部

## 第九步：测试回顾详情

1. 点击一条历史回顾
2. 查看详情页

**应该看到**：
- AI生成的内容
- 主题
- 统计信息（想法数、活跃天数、分类数）
- 原始想法列表（只包含生成时使用的记录）

## 第十步：测试分享卡片

1. 在回顾详情页
2. 点击"查看分享卡片"
3. **应该看到完整的卡片**，包含：
   - 标题"⚡ 闪念盒子"
   - 模式和主题
   - AI内容
   - 统计信息

**如果看到代码或乱码**：
1. 按 `F12` 查看控制台错误
2. 检查 localStorage：
```javascript
console.log(localStorage.getItem('shareCardData'))
```

## 常见问题排查

### 问题：后端启动失败
**检查**：
```bash
cd d:\Cursor\sparkbox\backend
python -c "from models.review import Review; print('模型导入成功')"
```

### 问题：前端请求失败
**检查**：
1. 后端是否在运行
2. 访问 http://localhost:8000/health
3. 应该返回 `{"status": "ok"}`

### 问题：数据库字段不存在
**重新运行迁移**：
```bash
cd d:\Cursor\sparkbox\backend
python migrate_reviews.py
```

## 验证清单

完成所有步骤后，验证：

- [ ] 数据库迁移成功
- [ ] 后端已重启并运行
- [ ] 前端缓存已清除
- [ ] 新建想法显示"刚刚"
- [ ] 选择分类后统计数字变化
- [ ] 生成回顾只包含选中分类
- [ ] 历史记录显示分类标签
- [ ] 历史记录显示正确的想法数量
- [ ] 回顾详情显示正确的记录
- [ ] 分享卡片正常显示

## 如果所有步骤都完成了还有问题

请提供以下信息：
1. 数据库迁移的输出
2. 后端启动的完整日志
3. 浏览器控制台的错误信息（截图）
4. Network 标签中的 API 请求详情（截图）
