<template>
  <view class="thought-card" @tap="$emit('tap', thought)" @longpress="$emit('longpress', thought)">
    <!-- 分类标识条 -->
    <view
      v-if="thought.category"
      class="category-bar"
      :style="{ background: thought.category.color }"
    />

    <view class="card-body">
      <!-- 分类标签 -->
      <view v-if="thought.category" class="category-badge" :style="{ color: thought.category.color, background: hexToLight(thought.category.color) }">
        <text>{{ thought.category.icon }}</text>
        <text class="cat-name">{{ thought.category.name }}</text>
      </view>

      <!-- 内容 -->
      <text class="content" :class="compact && 'compact'">{{ thought.content }}</text>

      <!-- AI 金句 -->
      <view v-if="thought.ai_quote" class="ai-quote">
        <text class="quote-icon">✦</text>
        <text class="quote-text">{{ thought.ai_quote }}</text>
      </view>

      <!-- 底部信息栏 -->
      <view class="footer">
        <view class="tags-row">
          <text v-for="(tag, i) in (thought.tags || []).slice(0, 3)" :key="i" class="tag-chip"># {{ tag }}</text>
        </view>
        <view class="meta">
          <text v-if="thought.mood" class="mood">{{ thought.mood }}</text>
          <text class="time">{{ formatTime(thought.created_at) }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
defineProps({
  thought: { type: Object, required: true },
  compact: { type: Boolean, default: false },
})
defineEmits(['tap', 'longpress'])

function formatTime(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  const now = new Date()
  const diff = now - d
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 86400000 * 2) return '昨天'
  return `${d.getMonth() + 1}/${d.getDate()}`
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
