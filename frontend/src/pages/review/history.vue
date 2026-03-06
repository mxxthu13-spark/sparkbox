<template>
  <div class="page">
    <!-- 头部 -->
    <div class="header">
      <div class="nav-back" @click="goBack">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="20" height="20">
          <polyline points="15 18 9 12 15 6"/>
        </svg>
      </div>
      <h1 class="title">历史回顾</h1>
      <div class="placeholder"></div>
    </div>

    <!-- 回顾列表 -->
    <div v-if="reviews.length > 0" class="reviews-list">
      <div
        v-for="review in reviews"
        :key="review.id"
        class="review-item"
        @click="openReview(review)"
      >
        <div class="review-header">
          <h3 class="review-title">{{ review.title }}</h3>
          <span class="review-date">{{ formatDate(review.created_at) }}</span>
        </div>
        
        <div class="review-info">
          <div class="info-row">
            <span class="info-label">📅 时间</span>
            <span class="info-value">{{ formatPeriod(review.period_start, review.period_end) }}</span>
          </div>
          
          <div v-if="review.category_ids && review.category_ids.length > 0" class="info-row">
            <span class="info-label">🏷️ 分类</span>
            <div class="category-tags">
              <span v-for="catId in review.category_ids.slice(0, 3)" :key="catId" class="category-tag">
                {{ getCategoryName(catId) }}
              </span>
              <span v-if="review.category_ids.length > 3" class="more-tag">+{{ review.category_ids.length - 3 }}</span>
            </div>
          </div>
          
          <div v-if="review.review_mode" class="info-row">
            <span class="info-label">✨ 模式</span>
            <span class="mode-badge" :class="`mode-${review.review_mode}`">{{ getModeLabel(review.review_mode) }}</span>
          </div>
          
          <div v-if="review.theme" class="info-row theme-row">
            <span class="info-label">💡 主题</span>
            <span class="theme-text">{{ review.theme }}</span>
          </div>
        </div>
        
        <div class="review-meta">
          <span class="meta-item">{{ review.thought_count }} 条想法</span>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <span class="empty-icon">📚</span>
      <p class="empty-text">还没有保存的回顾</p>
      <p class="empty-hint">生成回顾后点击"保存回顾"即可保存</p>
    </div>

    <BottomNav />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../../utils/api'
import { useThoughtsStore } from '../../store/thoughts'
import BottomNav from '../../components/BottomNav.vue'

const router = useRouter()
const thoughtsStore = useThoughtsStore()
const reviews = ref([])
const loading = ref(false)

function goBack() {
  router.back()
}

async function loadReviews() {
  loading.value = true
  try {
    await thoughtsStore.fetchCategories()
    const res = await api.reviews.list({ page: 1, page_size: 50 })
    reviews.value = res.items || []
  } catch (e) {
    uni.showToast({ title: e.message || '加载失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}

function openReview(review) {
  uni.navigateTo({ url: `/pages/review/detail?id=${review.id}` })
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
}

function formatPeriod(start, end) {
  if (!start || !end) return ''
  const s = new Date(start)
  const e = new Date(end)
  return `${s.getMonth() + 1}/${s.getDate()} - ${e.getMonth() + 1}/${e.getDate()}`
}

function getCategoryName(catId) {
  const cat = thoughtsStore.categories.find(c => c.id === catId)
  return cat ? `${cat.icon} ${cat.name}` : ''
}

function getModeLabel(mode) {
  const labels = {
    summary: '摘要模式',
    insight: '洞察模式',
    soul: '灵魂模式'
  }
  return labels[mode] || mode
}

onMounted(() => {
  loadReviews()
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #f9fafb;
  padding-bottom: 80px;
}

.header {
  background: #fff;
  padding: 12px 16px;
  border-bottom: 1px solid #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 10;
}

.nav-back {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #374151;
  border-radius: 8px;
  
  &:active {
    background: #f3f4f6;
  }
}

.title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.placeholder {
  width: 36px;
}

.reviews-list {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.review-item {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #f3f4f6;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transform: translateY(-2px);
  }

  &:active {
    transform: translateY(0);
  }
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.review-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0;
  flex: 1;
}

.review-date {
  font-size: 12px;
  color: #9ca3af;
  flex-shrink: 0;
  margin-left: 12px;
}

.review-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 8px;
  
  &.theme-row {
    align-items: flex-start;
  }
}

.info-label {
  font-size: 12px;
  color: #6b7280;
  flex-shrink: 0;
  min-width: 60px;
}

.info-value {
  font-size: 13px;
  color: #374151;
}

.category-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  align-items: center;
}

.category-tag {
  font-size: 11px;
  color: #6366f1;
  background: #ede9fe;
  padding: 3px 8px;
  border-radius: 8px;
}

.more-tag {
  font-size: 11px;
  color: #9ca3af;
  background: #f3f4f6;
  padding: 3px 8px;
  border-radius: 8px;
}

.mode-badge {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 10px;
  font-weight: 500;
  
  &.mode-summary {
    color: #dc2626;
    background: #fee2e2;
  }
  
  &.mode-insight {
    color: #2563eb;
    background: #dbeafe;
  }
  
  &.mode-soul {
    color: #7c3aed;
    background: #ede9fe;
  }
}

.theme-text {
  font-size: 13px;
  color: #166534;
  background: #f0fdf4;
  padding: 6px 10px;
  border-radius: 8px;
  line-height: 1.4;
  flex: 1;
}

.review-meta {
  display: flex;
  gap: 12px;
  padding-top: 8px;
  border-top: 1px solid #f3f4f6;
}

.meta-item {
  font-size: 12px;
  color: #6b7280;
  padding: 4px 10px;
  background: #f9fafb;
  border-radius: 12px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 100px 40px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 18px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 8px;
}

.empty-hint {
  font-size: 14px;
  color: #9ca3af;
  margin: 0;
  text-align: center;
}
</style>
