<template>
  <div class="page">
    <div v-if="review" class="content">
      <!-- 头部 -->
      <div class="header">
        <div class="nav-back" @click="goBack">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="20" height="20">
            <polyline points="15 18 9 12 15 6"/>
          </svg>
        </div>
        <h1 class="title">回顾详情</h1>
        <div class="placeholder"></div>
      </div>

      <!-- 回顾卡片 -->
      <div class="review-card">
        <div class="card-header">
          <h2 class="card-title">{{ review.title }}</h2>
          <div class="card-period">{{ formatPeriod(review.period_start, review.period_end) }}</div>
        </div>

        <!-- AI 内容 -->
        <div v-if="review.ai_content" class="ai-section">
          <div class="section-header">
            <span class="section-icon">✨</span>
            <span class="section-title">AI {{ getModeLabel(review.review_mode) }}</span>
          </div>
          <p class="ai-content">{{ review.ai_content }}</p>
        </div>

        <!-- 主题 -->
        <div v-if="review.theme" class="theme-section">
          <div class="section-header">
            <span class="section-icon">💡</span>
            <span class="section-title">长期主题</span>
          </div>
          <p class="theme-content">{{ review.theme }}</p>
        </div>
      </div>

      <!-- 原始想法列表 -->
      <div class="thoughts-section">
        <div class="section-header">
          <span class="section-icon">📝</span>
          <span class="section-title">原始想法</span>
          <span class="thoughts-count">{{ thoughts.length }} 条</span>
        </div>

        <div v-if="thoughts.length === 0" class="empty-thoughts">
          <span>暂无想法记录</span>
        </div>

        <div v-else class="thoughts-list">
          <div
            v-for="(t, i) in thoughts"
            :key="t.id"
            class="thought-card"
            @click="openThought(t)"
          >
            <div class="thought-header">
              <span class="thought-index">{{ i + 1 }}</span>
              <span class="thought-date">{{ formatDate(t.created_at) }}</span>
            </div>
            <p class="thought-content">{{ t.content }}</p>
            <div v-if="t.tags && t.tags.length" class="thought-tags">
              <span v-for="(tag, j) in t.tags.slice(0, 3)" :key="j" class="thought-tag">#{{ tag }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 分类信息 -->
      <div v-if="review.category_ids && review.category_ids.length > 0" class="categories-section-bottom">
        <div class="section-header">
          <span class="section-icon">🏷️</span>
          <span class="section-title">涉及分类</span>
        </div>
        <div class="category-tags">
          <span v-for="catId in review.category_ids" :key="catId" class="category-tag">
            {{ getCategoryName(catId) }}
          </span>
        </div>
      </div>

      <!-- 底部操作 -->
      <div class="bottom-actions">
        <button class="action-btn danger-btn" @click="confirmDelete">
          <span>🗑️ 删除回顾</span>
        </button>
      </div>
    </div>

    <div v-else class="loading-state">
      <span>加载中...</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../../utils/api'
import { useThoughtsStore } from '../../store/thoughts'

const route = useRoute()
const router = useRouter()
const thoughtsStore = useThoughtsStore()
const review = ref(null)
const thoughts = ref([])

const reviewId = route.query.id

const activeDays = computed(() => {
  if (!thoughts.value.length) return 0
  const days = new Set(thoughts.value.map((t) => t.created_at?.split('T')[0].split(' ')[0]))
  return days.size
})

function goBack() {
  router.back()
}

function getCategoryName(catId) {
  const cat = thoughtsStore.categories.find(c => c.id === catId)
  return cat ? `${cat.icon} ${cat.name}` : '未知分类'
}

async function loadReview() {
  try {
    await thoughtsStore.fetchCategories()
    const res = await api.reviews.get(reviewId)
    review.value = res
    thoughts.value = res.thoughts || []
    console.log('加载回顾详情:', res)
  } catch (e) {
    console.error('加载失败:', e)
    uni.showToast({ title: '加载失败', icon: 'none' })
    router.back()
  }
}

function openThought(t) {
  uni.navigateTo({ url: `/pages/thought/detail?id=${t.id}` })
}

function viewShareCard() {
  if (!review.value) return
  
  // 通过localStorage传递数据，避免URL长度限制
  const cardData = {
    mode: review.value.review_mode || 'insight',
    theme: review.value.theme || '',
    content: review.value.ai_content || '',
    thought_count: review.value.thought_count || 0,
    days: activeDays.value || 0,
    categories: review.value.category_ids?.length || 0,
  }
  
  console.log('传递卡片数据:', cardData)
  localStorage.setItem('shareCardData', JSON.stringify(cardData))
  uni.navigateTo({ url: '/pages/review/card' })
}

async function confirmDelete() {
  uni.showModal({
    title: '确认删除',
    content: '删除后无法恢复，确定要删除这条回顾吗？',
    success: async (res) => {
      if (res.confirm) {
        await deleteReview()
      }
    }
  })
}

async function deleteReview() {
  try {
    await api.reviews.delete(reviewId)
    uni.showToast({ title: '删除成功', icon: 'none' })
    setTimeout(() => {
      router.back()
    }, 1000)
  } catch (e) {
    uni.showToast({ title: e.message || '删除失败', icon: 'none' })
  }
}

function getModeLabel(mode) {
  const labels = {
    summary: '摘要',
    insight: '洞察',
    soul: '灵魂拷问'
  }
  return labels[mode] || '回顾'
}

function formatPeriod(start, end) {
  if (!start) return ''
  const s = new Date(start)
  const e = new Date(end)
  return `${s.getMonth() + 1}月${s.getDate()}日 至 ${e.getMonth() + 1}月${e.getDate()}日`
}

function formatDate(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  return `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

onMounted(() => {
  if (!reviewId) {
    router.back()
    return
  }
  loadReview()
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #f8f8fa;
  padding-bottom: 100px;
}

.content {
  max-width: 800px;
  margin: 0 auto;
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

.review-card {
  background: #fff;
  margin: 16px;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.card-header {
  margin-bottom: 20px;
}

.card-title {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 8px;
}

.card-period {
  font-size: 14px;
  color: #6b7280;
}

.categories-section {
  margin-bottom: 20px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
}

.categories-section-bottom {
  margin: 16px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
}

.category-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 8px;
}

.category-tag {
  font-size: 13px;
  color: #6366f1;
  background: #ede9fe;
  padding: 6px 12px;
  border-radius: 12px;
  font-weight: 500;
}

.ai-section {
  margin-bottom: 20px;
  padding: 20px;
  background: #f9fafb;
  border-radius: 12px;
  border-left: 4px solid #6366f1;
}

.theme-section {
  margin-bottom: 20px;
  padding: 20px;
  background: #f0fdf4;
  border-radius: 12px;
  border-left: 4px solid #10b981;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.section-icon {
  font-size: 18px;
}

.section-title {
  font-size: 15px;
  font-weight: 600;
  color: #374151;
}

.ai-content, .theme-content {
  font-size: 15px;
  line-height: 1.8;
  color: #4b5563;
  margin: 0;
  white-space: pre-wrap;
}

.thoughts-section {
  margin: 16px;
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.thoughts-count {
  margin-left: auto;
  font-size: 13px;
  color: #9ca3af;
  background: #f3f4f6;
  padding: 4px 12px;
  border-radius: 12px;
}

.empty-thoughts {
  text-align: center;
  padding: 40px;
  color: #9ca3af;
  font-size: 14px;
}

.thoughts-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 16px;
}

.thought-card {
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #f3f4f6;

  &:hover {
    background: #f3f4f6;
    transform: translateX(4px);
  }

  &:active {
    transform: translateX(2px);
  }
}

.thought-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.thought-index {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #6366f1;
  color: #fff;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.thought-date {
  font-size: 12px;
  color: #9ca3af;
}

.thought-content {
  font-size: 15px;
  line-height: 1.6;
  color: #374151;
  margin: 0 0 8px;
}

.thought-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.thought-tag {
  font-size: 12px;
  color: #6366f1;
  opacity: 0.7;
}

.bottom-actions {
  margin: 16px;
  display: flex;
  gap: 12px;
  justify-content: center;
}

.action-btn {
  flex: 1;
  max-width: 500px;
  height: 52px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;

  &:active {
    transform: scale(0.98);
  }
}

.primary-btn {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;

  &:hover {
    opacity: 0.9;
  }
}

.danger-btn {
  background: #fff;
  color: #ef4444;
  border: 2px solid #ef4444;

  &:hover {
    background: #fef2f2;
  }
}

.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  color: #9ca3af;
}
</style>
