<template>
  <div class="page">
    <!-- 顶部标题 -->
    <div class="header">
      <h1 class="title">回顾</h1>
    </div>

    <!-- 筛选条件 -->
    <div class="filters">
      <!-- 时间范围 -->
      <div class="filter-section">
        <label class="filter-label">时间范围</label>
        <div class="time-range">
          <input type="date" v-model="startDate" @change="checkThoughtCount" class="date-input" />
          <span class="range-separator">至</span>
          <input type="date" v-model="endDate" @change="checkThoughtCount" class="date-input" />
        </div>
      </div>

      <!-- 分类选择 -->
      <div class="filter-section">
        <label class="filter-label">选择分类（可多选）</label>
        <div class="category-chips">
          <div
            v-for="cat in categories"
            :key="cat.id"
            :class="['category-chip', selectedCategories.includes(cat.id) && 'active']"
            :style="selectedCategories.includes(cat.id) ? { background: cat.color, borderColor: cat.color, color: '#fff' } : {}"
            @click="toggleCategory(cat.id)"
          >
            <span>{{ cat.icon }} {{ cat.name }}</span>
          </div>
        </div>
      </div>

      <!-- 生成按钮 -->
      <button class="generate-btn" @click="generateReview" :disabled="generating">
        <span v-if="!generating">✦ AI 生成回顾</span>
        <span v-else>AI 思考中...</span>
      </button>

      <!-- 记录数量提示 -->
      <div class="count-hint">
        <span v-if="thoughtCount >= 0" :class="thoughtCount === 0 ? 'no-data' : ''">
          找到 {{ thoughtCount }} 条想法记录
        </span>
      </div>
      
      <div class="usage-hint">
        💡 提示：选择时间范围和分类后，点击"AI 生成回顾"按钮
      </div>
    </div>

    <!-- AI 生成的回顾卡片 -->
    <div v-if="reviewResult" class="review-cards">
      <!-- 根据用户选择的模式显示对应卡片 -->
      <div v-if="currentMode === 'summary'" ref="reviewCardRef" class="review-card summary-card">
        <div class="card-decoration">
          <div class="decoration-circle"></div>
          <div class="decoration-line"></div>
        </div>
        <div class="card-brand">
          <h2 class="brand-title">
            <svg class="logo-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            闪念盒子
          </h2>
          <div class="card-meta">
            <span class="meta-theme">{{ reviewResult.theme || '思想回顾' }}</span>
          </div>
        </div>
        <p class="card-content">{{ reviewResult.summary }}</p>
        
        <div class="card-footer">
          <button class="action-btn save-btn" @click="saveReview">保存回顾</button>
          <button class="action-btn share-btn" @click="saveAsImage">保存图片</button>
        </div>
      </div>

      <div v-if="currentMode === 'insight'" ref="reviewCardRef" class="review-card insight-card">
        <div class="card-decoration">
          <div class="decoration-circle"></div>
          <div class="decoration-line"></div>
        </div>
        <div class="card-brand">
          <h2 class="brand-title">
            <svg class="logo-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            闪念盒子
          </h2>
          <div class="card-meta">
            <span class="meta-theme">{{ reviewResult.theme || '思想回顾' }}</span>
          </div>
        </div>
        <p class="card-content">{{ reviewResult.insight }}</p>
        
        <div class="card-footer">
          <button class="action-btn save-btn" @click="saveReview">保存回顾</button>
          <button class="action-btn share-btn" @click="saveAsImage">保存图片</button>
        </div>
      </div>

      <div v-if="currentMode === 'soul'" ref="reviewCardRef" class="review-card soul-card">
        <div class="card-decoration">
          <div class="decoration-circle"></div>
          <div class="decoration-line"></div>
        </div>
        <div class="card-brand">
          <h2 class="brand-title">
            <svg class="logo-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            闪念盒子
          </h2>
          <div class="card-meta">
            <span class="meta-theme">{{ reviewResult.theme || '思想回顾' }}</span>
          </div>
        </div>
        <p class="card-content">{{ reviewResult.soul }}</p>
        
        <div class="card-footer">
          <button class="action-btn save-btn" @click="saveReview">保存回顾</button>
          <button class="action-btn share-btn" @click="saveAsImage">保存图片</button>
        </div>
      </div>

      <!-- 统计信息 -->
      <div class="stats-card">
        <div class="stat-item">
          <span class="stat-value">{{ reviewResult.thought_count || 0 }}</span>
          <span class="stat-label">条想法</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ reviewResult.days || 0 }}</span>
          <span class="stat-label">活跃天</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ reviewResult.categories || 0 }}</span>
          <span class="stat-label">个分类</span>
        </div>
      </div>
    </div>

    <!-- 历史回顾 -->
    <div v-if="historyReviews.length > 0" class="history-section">
      <div class="history-header">
        <h2 class="history-title">📚 历史回顾</h2>
        <span class="history-count">{{ historyReviews.length }} 条</span>
      </div>
      <div class="history-list">
        <div
          v-for="review in historyReviews"
          :key="review.id"
          class="history-item"
          @click="openHistoryReview(review)"
        >
          <div class="history-item-header">
            <span class="history-date">{{ formatHistoryDate(review.period_start, review.period_end) }}</span>
            <span class="history-count-badge">{{ review.thought_count }} 条</span>
          </div>
          <p class="history-preview">{{ review.title }}</p>
          <div v-if="review.category_ids && review.category_ids.length > 0" class="history-categories">
            <span v-for="catId in review.category_ids.slice(0, 3)" :key="catId" class="history-category-tag">
              {{ getCategoryName(catId) }}
            </span>
            <span v-if="review.category_ids.length > 3" class="history-more-tag">+{{ review.category_ids.length - 3 }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="!reviewResult && !generating" class="empty-state">
      <span class="empty-icon">🌟</span>
      <span class="empty-text">选择时间和分类，AI 帮你看看思想的轨迹</span>
    </div>

    <!-- 底部导航 -->
    <BottomNav />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useThoughtsStore } from '../../store/thoughts'
import { api } from '../../utils/api'
import html2canvas from 'html2canvas'
import BottomNav from '../../components/BottomNav.vue'

const thoughtsStore = useThoughtsStore()

const startDate = ref(getDefaultStartDate())
const endDate = ref(getDefaultEndDate())
const selectedCategories = ref([])
const generating = ref(false)
const reviewResult = ref(null)
const currentMode = ref(localStorage.getItem('reviewStyle') || 'insight')  // 默认洞察模式
const thoughtCount = ref(0)  // 记录数量，默认0
const reviewCardRef = ref(null)  // 卡片元素引用
const historyReviews = ref([])  // 历史回顾列表

const categories = computed(() => thoughtsStore.categories)

function getDefaultStartDate() {
  const date = new Date()
  date.setDate(date.getDate() - 30) // 默认最近30天
  return date.toISOString().split('T')[0]
}

function getDefaultEndDate() {
  return new Date().toISOString().split('T')[0]
}

function toggleCategory(id) {
  const index = selectedCategories.value.indexOf(id)
  if (index > -1) {
    selectedCategories.value.splice(index, 1)
  } else {
    selectedCategories.value.push(id)
  }
  // 分类变化时查询记录数量
  checkThoughtCount()
}

async function checkThoughtCount() {
  if (!startDate.value || !endDate.value) return
  
  try {
    const params = {
      start_date: startDate.value,
      end_date: endDate.value,
      page: 1,
      page_size: 1, // 只需要获取总数
    }
    
    // 如果选择了分类，添加分类筛选参数
    if (selectedCategories.value.length > 0) {
      params.category_ids = selectedCategories.value.join(',')
    }
    
    console.log('查询想法数量，参数:', params)
    const res = await api.thoughts.list(params)
    thoughtCount.value = res.total || 0
    console.log('查询结果: 共', res.total, '条想法')
  } catch (e) {
    console.error('查询想法数量失败:', e)
    thoughtCount.value = 0
  }
}

async function generateReview() {
  if (generating.value) return
  
  if (!startDate.value || !endDate.value) {
    uni.showToast({ title: '请选择时间范围', icon: 'none' })
    return
  }

  generating.value = true
  reviewResult.value = null

  try {
    // 获取用户选择的回顾风格
    currentMode.value = localStorage.getItem('reviewStyle') || 'insight'
    
    // 构建请求参数
    const requestData = {
      start_date: startDate.value,
      end_date: endDate.value,
      style: currentMode.value,
    }
    
    // 如果选择了分类，添加分类筛选
    if (selectedCategories.value.length > 0) {
      requestData.category_ids = selectedCategories.value
    }
    
    console.log('生成回顾请求参数:', requestData)
    
    // 调用后端 API 生成回顾
    const result = await api.ai.generateReview(requestData)
    
    console.log('生成回顾结果:', result)
    reviewResult.value = result
    uni.showToast({ title: 'AI 回顾已生成', icon: 'none' })
  } catch (e) {
    console.error('生成回顾失败:', e)
    uni.showToast({ title: e.message || '生成失败', icon: 'none' })
  } finally {
    generating.value = false
  }
}

function saveAsCard() {
  if (!reviewResult.value) return
  
  let content = ''
  let title = ''
  
  if (currentMode.value === 'summary') {
    title = '📝 摘要模式'
    content = reviewResult.value.summary
  } else if (currentMode.value === 'insight') {
    title = '💡 洞察模式'
    content = reviewResult.value.insight
  } else if (currentMode.value === 'soul') {
    title = '✨ 灵魂模式'
    content = reviewResult.value.soul
  }
  
  if (reviewResult.value.theme) {
    content += `\n\n【长期主题】\n${reviewResult.value.theme}`
  }
  
  const encodedContent = encodeURIComponent(`${title}\n\n${content}`)
  uni.navigateTo({ url: `/pages/card/create?content=${encodedContent}` })
}

async function saveReview() {
  if (!reviewResult.value) return
  
  try {
    // 获取当前模式的内容
    const modeNames = {
      summary: '摘要模式',
      insight: '洞察模式',
      soul: '灵魂模式'
    }
    
    const modeContent = {
      summary: reviewResult.value.summary,
      insight: reviewResult.value.insight,
      soul: reviewResult.value.soul
    }
    
    const title = reviewResult.value.theme || `${modeNames[currentMode.value]}回顾`
    const aiContent = modeContent[currentMode.value] || ''
    
    console.log('保存回顾，参数:', {
      period_start: startDate.value,
      period_end: endDate.value,
      title: title,
      category_ids: selectedCategories.value,
      theme: reviewResult.value.theme,
      review_mode: currentMode.value,
      ai_content: aiContent,
    })
    
    await api.reviews.generate({
      period_type: 'custom',
      period_start: startDate.value,
      period_end: endDate.value,
      title: title,
      category_ids: selectedCategories.value.length > 0 ? selectedCategories.value : null,
      theme: reviewResult.value.theme,
      review_mode: currentMode.value,
      ai_content: aiContent,  // 确保传递 AI 内容
    })
    
    // 保存成功后重新加载历史列表
    await loadHistoryReviews()
    uni.showToast({ title: '回顾已保存', icon: 'none' })
  } catch (e) {
    console.error('保存回顾失败:', e)
    uni.showToast({ title: e.message || '保存失败', icon: 'none' })
  }
}

async function saveAsImage() {
  if (!reviewCardRef.value) {
    uni.showToast({ title: '卡片未加载', icon: 'none' })
    return
  }

  try {
    uni.showLoading({ title: '生成图片中...' })
    
    // 隐藏按钮
    const footer = reviewCardRef.value.querySelector('.card-footer')
    if (footer) {
      footer.style.display = 'none'
    }
    
    // 使用 html2canvas 将卡片转换为图片
    const canvas = await html2canvas(reviewCardRef.value, {
      backgroundColor: null,
      scale: 2, // 提高清晰度
      useCORS: true,
      logging: false,
    })
    
    // 恢复按钮显示
    if (footer) {
      footer.style.display = 'flex'
    }
    
    // 转换为 blob
    canvas.toBlob(async (blob) => {
      try {
        // 创建下载链接
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        const timestamp = new Date().getTime()
        link.download = `回顾-${currentMode.value}-${timestamp}.png`
        link.href = url
        link.click()
        
        // 清理
        URL.revokeObjectURL(url)
        
        uni.hideLoading()
        uni.showToast({ title: '图片已保存', icon: 'none' })
      } catch (e) {
        uni.hideLoading()
        uni.showToast({ title: '保存失败', icon: 'none' })
      }
    }, 'image/png')
  } catch (e) {
    uni.hideLoading()
    uni.showToast({ title: e.message || '生成失败', icon: 'none' })
  }
}

async function loadHistoryReviews() {
  try {
    const res = await api.reviews.list({ page: 1, page_size: 10 })
    historyReviews.value = res.items || []
  } catch (e) {
    console.error('加载历史回顾失败:', e)
  }
}

function openHistoryReview(review) {
  uni.navigateTo({ url: `/pages/review/detail?id=${review.id}` })
}

function formatHistoryDate(start, end) {
  if (!start || !end) return ''
  const s = new Date(start)
  const e = new Date(end)
  return `${s.getMonth() + 1}/${s.getDate()} - ${e.getMonth() + 1}/${e.getDate()}`
}

function getCategoryName(catId) {
  const cat = thoughtsStore.categories.find(c => c.id === catId)
  return cat ? `${cat.icon} ${cat.name}` : '未知'
}

onMounted(async () => {
  await thoughtsStore.fetchCategories()
  await checkThoughtCount()  // 初始化时查询记录数量
  await loadHistoryReviews()  // 加载历史回顾
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #f8f8fa;
  padding-bottom: 80px;
}

.header {
  background: #fff;
  padding: 24px 20px;
  border-bottom: 1px solid #f3f4f6;
}

.title {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.filters {
  background: #fff;
  padding: 20px;
  margin: 16px;
  border-radius: 12px;
}

.filter-section {
  margin-bottom: 20px;

  &:last-of-type {
    margin-bottom: 24px;
  }
}

.filter-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 12px;
}

.time-range {
  display: flex;
  align-items: center;
  gap: 12px;
}

.date-input {
  flex: 1;
  height: 44px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0 12px;
  font-size: 15px;
  color: #374151;

  &:focus {
    outline: none;
    border-color: #6366f1;
  }
}

.range-separator {
  font-size: 14px;
  color: #9ca3af;
}

.category-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.category-chip {
  padding: 8px 16px;
  border-radius: 20px;
  border: 1.5px solid #e5e7eb;
  background: #f9fafb;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;

  &:active {
    transform: scale(0.95);
  }

  &.active {
    font-weight: 500;
  }
}

.generate-btn {
  width: 100%;
  height: 48px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    opacity: 0.9;
  }

  &:disabled {
    background: #9ca3af;
    cursor: not-allowed;
  }
}

.count-hint {
  margin-top: 12px;
  text-align: center;
  font-size: 14px;
  color: #6b7280;
  padding: 8px;
  background: #f9fafb;
  border-radius: 8px;

  .no-data {
    color: #ef4444;
  }
}

.usage-hint {
  margin-top: 8px;
  text-align: center;
  font-size: 13px;
  color: #9ca3af;
  padding: 6px;
}

.review-cards {
  padding: 0 16px 16px;
}

.review-card {
  background: linear-gradient(135deg, #fdfcfb 0%, #f7f6f4 100%);
  border-radius: 20px;
  padding: 32px 24px;
  margin-bottom: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.summary-card {
  background: linear-gradient(135deg, #fff5f5 0%, #ffe9e9 100%);
  border-left: 4px solid #f87171;
}

.insight-card {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-left: 4px solid #60a5fa;
}

.soul-card {
  background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
  border-left: 4px solid #a78bfa;
}

.card-decoration {
  position: absolute;
  top: 0;
  right: 0;
  opacity: 0.1;
  pointer-events: none;
}

.decoration-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, transparent 70%);
  position: absolute;
  top: -40px;
  right: -40px;
}

.decoration-line {
  width: 200px;
  height: 2px;
  background: linear-gradient(90deg, transparent 0%, rgba(99, 102, 241, 0.3) 50%, transparent 100%);
  position: absolute;
  top: 60px;
  right: -50px;
  transform: rotate(-45deg);
}

.card-brand {
  margin-bottom: 24px;
  text-align: center;
}

.brand-title {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 12px;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.logo-icon {
  width: 28px;
  height: 28px;
  color: #6366f1;
  flex-shrink: 0;
}

.card-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
}

.meta-theme {
  color: #6b7280;
  font-weight: 500;
}

.card-content {
  font-size: 16px;
  line-height: 1.8;
  color: #374151;
  margin: 0 0 24px;
  white-space: pre-wrap;
  font-weight: 400;
}

.key-points {
  margin-bottom: 24px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  border-left: 3px solid #6366f1;
}

.points-header {
  font-size: 14px;
  font-weight: 600;
  color: #6366f1;
  margin-bottom: 16px;
}

.points-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.point-item {
  display: flex;
  gap: 8px;
  align-items: flex-start;
}

.point-bullet {
  font-size: 20px;
  color: #6366f1;
  line-height: 1.6;
  flex-shrink: 0;
  font-weight: bold;
}

.point-text {
  flex: 1;
  font-size: 14px;
  line-height: 1.6;
  color: #4b5563;
  margin: 0;
}

.card-theme {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 12px;
  margin-bottom: 20px;
  backdrop-filter: blur(10px);
}

.theme-icon {
  font-size: 20px;
  flex-shrink: 0;
  margin-top: 2px;
}

.theme-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.theme-label {
  font-size: 12px;
  color: #9ca3af;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.theme-text {
  font-size: 15px;
  color: #6366f1;
  font-weight: 500;
  line-height: 1.6;
}

.card-footer {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.action-btn {
  flex: 1;
  height: 44px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;

  &:active {
    transform: scale(0.98);
  }
}

.save-btn {
  background: #6366f1;
  color: #fff;

  &:hover {
    background: #5558e3;
  }
}

.share-btn {
  background: #fff;
  color: #6366f1;
  border: 2px solid #6366f1;

  &:hover {
    background: #f5f3ff;
  }
}

.original-thoughts {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 2px dashed rgba(0, 0, 0, 0.1);
}

.thoughts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.thoughts-title {
  font-size: 15px;
  font-weight: 600;
  color: #6b7280;
}

.thoughts-count {
  font-size: 13px;
  color: #9ca3af;
  background: rgba(0, 0, 0, 0.05);
  padding: 4px 12px;
  border-radius: 12px;
}

.thoughts-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.thought-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  transition: all 0.2s;

  &:hover {
    background: rgba(255, 255, 255, 0.8);
  }
}

.thought-index {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(99, 102, 241, 0.1);
  color: #6366f1;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 600;
}

.thought-text {
  flex: 1;
  font-size: 14px;
  line-height: 1.6;
  color: #4b5563;
  margin: 0;
}

.stats-card {
  margin-bottom: 6px;
}

.history-section {
  padding: 0 16px 16px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 0 4px;
}

.history-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.history-count {
  font-size: 13px;
  color: #9ca3af;
  background: #f3f4f6;
  padding: 4px 12px;
  border-radius: 12px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-item {
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

.history-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.history-date {
  font-size: 14px;
  font-weight: 600;
  color: #6366f1;
}

.history-count-badge {
  font-size: 12px;
  color: #6b7280;
  background: #f9fafb;
  padding: 4px 10px;
  border-radius: 10px;
}

.history-preview {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.history-categories {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-top: 8px;
}

.history-category-tag {
  font-size: 11px;
  color: #6366f1;
  background: #ede9fe;
  padding: 3px 8px;
  border-radius: 8px;
}

.history-more-tag {
  font-size: 11px;
  color: #9ca3af;
  background: #f3f4f6;
  padding: 3px 8px;
  border-radius: 8px;
}

.theme-text {
  font-size: 14px;
  color: #111827;
  line-height: 1.6;
}

.save-card-btn {
  width: 100%;
  height: 40px;
  background: #f3f4f6;
  color: #6b7280;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: #e5e7eb;
  }
}

.stats-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  justify-content: space-around;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #6366f1;
}

.stat-label {
  font-size: 13px;
  color: #9ca3af;
  margin-top: 4px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 15px;
  color: #9ca3af;
  text-align: center;
}
</style>
