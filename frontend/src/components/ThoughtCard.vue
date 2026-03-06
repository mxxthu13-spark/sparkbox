<template>
  <div class="thought-card" @tap="$emit('tap', thought)" @longpress="$emit('longpress', thought)">
    <!-- 分类标识条 -->
    <div
      v-if="thought.category"
      class="category-bar"
      :style="{ background: thought.category.color }"
    />

    <div class="card-body">
      <!-- 分类标签 -->
      <div v-if="thought.category" class="category-badge" :style="{ color: thought.category.color, background: hexToLight(thought.category.color) }">
        <span>{{ thought.category.icon }}</span>
        <span class="cat-name">{{ thought.category.name }}</span>
      </div>

      <!-- 内容 -->
      <span class="content" :class="compact && 'compact'">{{ thought.content }}</span>

      <!-- AI 金句 -->
      <div v-if="thought.ai_quote" class="ai-quote">
        <span class="quote-icon">✦</span>
        <span class="quote-text">{{ thought.ai_quote }}</span>
      </div>

      <!-- 底部信息栏 -->
      <div class="footer">
        <div class="tags-row">
          <span v-for="(tag, i) in (thought.tags || []).slice(0, 3)" :key="i" class="tag-chip"># {{ tag }}</span>
        </div>
        <div class="meta">
          <span v-if="thought.mood" class="mood">{{ thought.mood }}</span>
          <span class="time">{{ formatTime(thought.created_at) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  thought: { type: Object, required: true },
  compact: { type: Boolean, default: false },
})
defineEmits(['tap', 'longpress'])

function formatTime(ts) {
  if (!ts) return ''
  
  try {
    // 强制当作本地时间处理
    let timeStr = String(ts)
    
    // 移除任何时区标记 (Z 或 +08:00 等)
    timeStr = timeStr.replace('Z', '').replace(/[+-]\d{2}:\d{2}$/, '')
    
    // 支持多种格式: 2026-03-06T10:00:00 或 2026-03-06 10:00:00
    const match = timeStr.match(/^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})/)
    if (!match) {
      console.warn('时间格式不匹配:', ts)
      return timeStr
    }
    
    // 手动构造本地时间（不使用 UTC）
    const d = new Date(
      parseInt(match[1]),      // year
      parseInt(match[2]) - 1,  // month (0-indexed)
      parseInt(match[3]),      // day
      parseInt(match[4]),      // hour
      parseInt(match[5]),      // minute
      parseInt(match[6])       // second
    )
    
    const now = new Date()
    const diff = now - d
    
    // 调试日志（生产环境可以删除）
    if (diff < 0 || diff > 86400000 * 365) {
      console.log('时间异常:', {
        原始: ts,
        解析: d.toString(),
        当前: now.toString(),
        差值小时: (diff / 3600000).toFixed(2)
      })
    }
    
    if (diff < 0) return `${d.getMonth() + 1}/${d.getDate()}`
    if (diff < 60000) return '刚刚'
    if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
    if (diff < 86400000 * 2) return '昨天'
    return `${d.getMonth() + 1}/${d.getDate()}`
  } catch (e) {
    console.error('时间解析错误:', e, ts)
    return String(ts)
  }
}

function hexToLight(hex) {
  try {
    const r = parseInt(hex.slice(1, 3), 16)
    const g = parseInt(hex.slice(3, 5), 16)
    const b = parseInt(hex.slice(5, 7), 16)
    return `rgba(${r},${g},${b},0.1)`
  } catch {
    return '#f0f0ff'
  }
}
</script>

<style lang="scss" scoped>
.thought-card {
  background: #fff;
  border-radius: 20rpx;
  margin-bottom: 20rpx;
  overflow: hidden;
  display: flex;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
  active-opacity: 0.9;
}

.category-bar {
  width: 8rpx;
  flex-shrink: 0;
}

.card-body {
  flex: 1;
  padding: 24rpx;
}

.category-badge {
  display: inline-flex;
  align-items: center;
  gap: 6rpx;
  padding: 4rpx 14rpx;
  border-radius: 100rpx;
  font-size: 22rpx;
  margin-bottom: 14rpx;
}

.cat-name {
  font-size: 22rpx;
}

.content {
  font-size: 30rpx;
  color: #111827;
  line-height: 1.7;
  display: block;

  &.compact {
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
  }
}

.ai-quote {
  display: flex;
  align-items: flex-start;
  gap: 8rpx;
  margin-top: 16rpx;
  padding: 14rpx 18rpx;
  background: #f5f3ff;
  border-radius: 12rpx;
  border-left: 4rpx solid #6366f1;
}

.quote-icon {
  color: #6366f1;
  font-size: 22rpx;
  flex-shrink: 0;
  margin-top: 2rpx;
}

.quote-text {
  font-size: 26rpx;
  color: #4338ca;
  line-height: 1.6;
  font-style: italic;
}

.footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-top: 16rpx;
}

.tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8rpx;
  flex: 1;
}

.tag-chip {
  font-size: 20rpx;
  color: #9ca3af;
}

.meta {
  display: flex;
  align-items: center;
  gap: 12rpx;
  flex-shrink: 0;
}

.mood {
  font-size: 26rpx;
}

.time {
  font-size: 22rpx;
  color: #9ca3af;
}
</style>

