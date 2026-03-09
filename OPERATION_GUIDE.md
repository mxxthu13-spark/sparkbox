# SparkBox 完整运营指南

## 📋 目录
1. [你的网站信息](#你的网站信息)
2. [后端管理](#后端管理)
3. [前端管理](#前端管理)
4. [日常运营](#日常运营)
5. [数据监控](#数据监控)
6. [分享给他人](#分享给他人)
7. [常见问题](#常见问题)
8. [成本说明](#成本说明)

---

## 🌐 你的网站信息

### 前端地址（用户访问）
- **网址**: https://sparkbox.vercel.app （或你的自定义域名）
- **用途**: 用户注册、登录、使用 SparkBox 的地方
- **分享**: 把这个网址发给朋友就可以了

### 后端地址（API 服务）
- **网址**: https://sparkbox-backend.onrender.com
- **用途**: 提供数据和 AI 功能
- **注意**: 普通用户不需要访问这个地址

### 代码仓库
- **GitHub**: https://github.com/mxxthu13-spark/sparkbox
- **用途**: 存储代码，更新功能

---

## 🖥️ 后端管理（Render）

### 后端会自动运行吗？
✅ **是的！** 后端会 24/7 自动运行，你不需要手动开启或关闭。

### 访问后端管理
1. 登录：https://render.com/
2. 点击 `sparkbox-backend` 项目
3. 可以看到：
   - **运行状态**：Live（运行中）/ Failed（失败）
   - **日志**：查看错误和访问记录
   - **重启**：如果出问题，点击 "Manual Deploy" → "Clear build cache & deploy"

### 后端免费计划限制
- ⏰ **15 分钟无活动会休眠**
  - 第一次访问会慢 30-60 秒（唤醒时间）
  - 之后访问正常速度
- 💾 **每月 750 小时免费**（够用）
- 📊 **数据库**: 免费 SQLite（数据存储在服务器上）

### 如何保持后端活跃？
如果不想休眠，可以：
1. 使用 UptimeRobot（免费）每 5 分钟 ping 一次
2. 访问：https://uptimerobot.com/
3. 添加监控：`https://sparkbox-backend.onrender.com/docs`

### 查看后端日志
1. Render Dashboard → `sparkbox-backend`
2. 点击 **"Logs"** 标签
3. 可以看到：
   - 用户访问记录
   - 错误信息
   - API 调用情况

### 修改环境变量
1. Render Dashboard → `sparkbox-backend`
2. 点击 **"Environment"**
3. 可以修改：
   - `DEEPSEEK_API_KEY`（如果 API Key 过期）
   - `DATABASE_URL`（数据库地址）
   - `SECRET_KEY`（安全密钥）

---

## 🎨 前端管理（Vercel）

### 前端会自动运行吗？
✅ **是的！** 前端会 24/7 自动运行，全球 CDN 加速。

### 访问前端管理
1. 登录：https://vercel.com/
2. 点击 `sparkbox` 项目
3. 可以看到：
   - **部署状态**：Ready（就绪）/ Building（构建中）
   - **访问量统计**
   - **域名管理**

### 前端免费计划限制
- 🌍 **无限带宽**（免费）
- 📈 **每月 100GB 流量**（够用）
- 🚀 **全球 CDN**（访问速度快）
- 🔄 **自动部署**（推送代码自动更新）

### 自定义域名
如果你有自己的域名（例如：sparkbox.com）：
1. Vercel Dashboard → `sparkbox` → **"Settings"** → **"Domains"**
2. 添加你的域名
3. 按照提示配置 DNS
4. 等待生效（几分钟到几小时）

### 查看访问统计
1. Vercel Dashboard → `sparkbox`
2. 点击 **"Analytics"** 标签
3. 可以看到：
   - 访问量（PV）
   - 访客数（UV）
   - 访问来源
   - 页面性能

---

## 📊 日常运营

### 每天需要做什么？
❌ **什么都不用做！** 网站会自动运行。

### 每周建议检查
1. **访问网站**：确保能正常打开
2. **测试功能**：注册、登录、创建想法
3. **查看日志**：Render 后端日志，看有没有错误

### 每月建议检查
1. **Render 使用量**：确保没超过免费额度
2. **Vercel 流量**：确保没超过 100GB
3. **DeepSeek API**：检查余额（如果用完需要充值）

### 如何更新功能？
如果你想修改代码：
1. 在本地修改代码
2. 推送到 GitHub：
   ```bash
   git add .
   git commit -m "更新说明"
   git push
   ```
3. Render 和 Vercel 会**自动检测并部署**
4. 等待 3-5 分钟，更新生效

---

## 📈 数据监控

### 用户数据在哪里？
- **存储位置**：Render 后端的 SQLite 数据库
- **访问方式**：通过 API 或数据库工具

### 如何查看用户数据？
**方法1：通过 API（推荐）**
1. 访问：https://sparkbox-backend.onrender.com/docs
2. 点击 **"Authorize"**，输入管理员 Token
3. 可以查看：
   - 用户列表
   - 想法数量
   - 回顾记录

**方法2：直接查看数据库**
1. Render Dashboard → `sparkbox-backend`
2. 点击 **"Shell"** 标签
3. 运行命令查看数据：
   ```bash
   sqlite3 sparkbox.db "SELECT COUNT(*) FROM users;"
   ```

### 关键指标
- **注册用户数**：有多少人注册
- **活跃用户数**：最近 7 天登录的用户
- **想法总数**：用户创建的想法数量
- **AI 调用次数**：DeepSeek API 使用量

### 设置监控告警
使用 **UptimeRobot**（免费）：
1. 访问：https://uptimerobot.com/
2. 添加监控：
   - URL: `https://sparkbox-backend.onrender.com/docs`
   - 类型: HTTP(s)
   - 间隔: 5 分钟
3. 设置告警：
   - 邮件通知
   - 如果网站挂了会收到邮件

---

## 👥 分享给他人

### 如何分享？
直接把前端网址发给朋友：
```
https://sparkbox.vercel.app
```

### 分享注意事项

#### ✅ 可以做的
- 分享给朋友、同事
- 在社交媒体发布
- 写教程、博客介绍
- 收集用户反馈

#### ⚠️ 需要注意的
1. **隐私保护**
   - 不要分享后端地址（`onrender.com`）
   - 不要泄露环境变量（API Key、Secret Key）
   - 不要公开数据库内容

2. **用户协议**
   - 告诉用户数据如何存储
   - 说明 AI 功能由 DeepSeek 提供
   - 提醒用户不要输入敏感信息

3. **成本控制**
   - 免费计划有限制
   - 如果用户太多，可能需要升级付费计划
   - DeepSeek API 需要充值

4. **功能说明**
   - 第一次访问可能慢（后端唤醒）
   - AI 功能需要网络
   - 数据存储在云端

### 推广建议
1. **小范围测试**：先给 5-10 个朋友试用
2. **收集反馈**：问他们哪里不好用
3. **逐步优化**：修复 bug，改进功能
4. **扩大推广**：功能稳定后再大范围分享

### 用户支持
如果用户遇到问题：
1. **常见问题**：准备一个 FAQ 文档
2. **联系方式**：提供邮箱或微信
3. **反馈渠道**：GitHub Issues 或问卷

---

## ❓ 常见问题

### Q1: 网站打不开怎么办？
**检查步骤**：
1. 访问 https://sparkbox.vercel.app（前端）
   - 如果打不开：检查 Vercel 状态
2. 访问 https://sparkbox-backend.onrender.com/docs（后端）
   - 如果打不开：检查 Render 状态
3. 查看 Render 日志，看有没有错误

**解决方法**：
- Render Dashboard → "Manual Deploy" → "Clear build cache & deploy"
- 等待 3-5 分钟重新部署

### Q2: 用户无法注册/登录？
**可能原因**：
1. 后端休眠（第一次访问慢）
2. 数据库连接失败
3. API Key 过期

**解决方法**：
1. 查看 Render 日志
2. 检查环境变量
3. 重新部署后端

### Q3: AI 功能不工作？
**可能原因**：
1. DeepSeek API Key 过期
2. API 余额不足
3. 网络问题

**解决方法**：
1. 登录 DeepSeek 检查余额
2. 更新 API Key（Render Environment）
3. 重新部署

### Q4: 如何备份数据？
**方法1：导出数据库**
1. Render Dashboard → `sparkbox-backend` → "Shell"
2. 运行：
   ```bash
   sqlite3 sparkbox.db .dump > backup.sql
   ```
3. 下载 `backup.sql`

**方法2：定期备份（推荐）**
- 升级到 Render 付费计划（自动备份）
- 或使用 PostgreSQL（Render 免费提供）

### Q5: 如何删除用户数据？
**通过 API**：
1. 访问：https://sparkbox-backend.onrender.com/docs
2. 使用管理员权限
3. 调用删除接口

**通过数据库**：
1. Render Shell
2. 运行 SQL：
   ```sql
   DELETE FROM users WHERE id = 'user_id';
   ```

### Q6: 网站被攻击怎么办？
**防护措施**：
1. **限流**：Render 和 Vercel 自带 DDoS 防护
2. **监控**：UptimeRobot 实时监控
3. **备份**：定期备份数据库

**如果被攻击**：
1. 暂时关闭服务（Render → Suspend）
2. 检查日志，找出攻击来源
3. 加强安全措施（添加验证码、限流）

---

## 💰 成本说明

### 当前成本：免费
- ✅ Render 免费计划：$0/月
- ✅ Vercel 免费计划：$0/月
- ✅ GitHub 免费计划：$0/月
- ⚠️ DeepSeek API：按使用量付费（需充值）

### DeepSeek API 费用
- **价格**：约 ¥0.001/1000 tokens
- **估算**：
  - 每次 AI 对话：约 ¥0.01-0.05
  - 100 个用户/月：约 ¥10-50
- **充值**：https://platform.deepseek.com/

### 何时需要升级付费？

#### Render 付费计划（$7/月）
**需要升级的情况**：
- 用户超过 100 人
- 需要后端不休眠
- 需要自动备份

#### Vercel 付费计划（$20/月）
**需要升级的情况**：
- 流量超过 100GB/月
- 需要更多并发
- 需要高级分析

### 成本优化建议
1. **初期**：使用免费计划（够用）
2. **增长期**：只升级 Render（$7/月）
3. **成熟期**：根据需要升级 Vercel

---

## 🎯 下一步建议

### 立即做的事
1. ✅ 测试所有功能（注册、登录、创建想法、AI 功能）
2. ✅ 设置 UptimeRobot 监控
3. ✅ 保存所有账号密码（GitHub、Render、Vercel、DeepSeek）
4. ✅ 分享给 3-5 个朋友测试

### 本周做的事
1. 📝 准备用户使用指南
2. 📝 准备 FAQ 文档
3. 🐛 收集 bug 和反馈
4. 🔧 修复问题

### 本月做的事
1. 📊 分析用户数据
2. 💡 优化功能
3. 📣 扩大推广
4. 💰 评估是否需要升级付费

---

## 📞 获取帮助

### 技术问题
- **GitHub Issues**: https://github.com/mxxthu13-spark/sparkbox/issues
- **Render 文档**: https://render.com/docs
- **Vercel 文档**: https://vercel.com/docs

### 平台状态
- **Render Status**: https://status.render.com/
- **Vercel Status**: https://www.vercel-status.com/
- **GitHub Status**: https://www.githubstatus.com/

---

## 🎉 恭喜你！

你已经成功部署了一个完整的 Web 应用！

**记住**：
- ✅ 网站会自动运行，不需要每天管理
- ✅ 定期检查状态和日志
- ✅ 收集用户反馈，持续改进
- ✅ 享受创造的乐趣！

**祝你运营顺利！** 🚀

---

*最后更新：2026-03-09*
