<template>
  <div class="page">
    <!-- 头部 -->
    <div class="header">
      <div class="nav-back" @click="goBack">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="20" height="20">
          <polyline points="15 18 9 12 15 6"/>
        </svg>
      </div>
      <h1 class="title">分享卡片</h1>
      <div class="placeholder"></div>
    </div>

    <!-- 卡片预览 -->
    <div class="card-container">
      <div ref="cardRef" class="review-card" :class="`${mode}-card`">
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
            <span class="meta-mode">{{ getModeLabel(mode) }}</span>
            <span class="meta-divider">·</span>
            <span class="meta-theme">{{ theme || '思想回顾' }}</span>
          </div>
        </div>
        
        <p class="card-content">{{ content }}</p>
        
        <!-- 统计信息 -->
        <div class="card-stats">
          <div class="stat-item">
            <span class="stat-value">{{ thoughtCount }}</span>
            <span class="stat-label">条想法</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-value">{{ days }}</span>
            <span class="stat-label">活跃天</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-value">{{ categories }}</span>
            <span class="stat-label">个分类</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="actions">
      <button class="action-btn" @click="saveAsImage">
        <span>💾 保存图片</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import html2canvas from 'html2canvas'

const router = useRouter()
const cardRef = ref(null)

const mode = ref('insight')
const theme = ref('')
const content = ref('')
const thoughtCount = ref(0)
const days = ref(0)
const categories = ref(0)

function goBack() {
  router.back()
}

function getModeLabel(m) {
  const labels = {
    summary: '摘要模式',
    insight: '洞察模式',
    soul: '灵魂模式'
  }
  return labels[m] || '回顾'
}

async function saveAsImage() {
  if (!cardRef.value) {
    uni.showToast({ title: '卡片未加载', icon: 'none' })
    return
  }

  try {
    uni.showLoading({ title: '生成图片中...' })
    
    const canvas = await html2canvas(cardRef.value, {
      backgroundColor: null,
      scale: 2,
      useCORS: true,
      logging: false,
    })
    
    canvas.toBlob(async (blob) => {
      try {
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        const timestamp = new Date().getTime()
        link.download = `闪念盒子-${mode.value}-${timestamp}.png`
        link.href = url
        link.click()
        
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

onMounted(() => {
  const storedData = localStorage.getItem('shareCardData')
  if (storedData) {
    try {
      const data = JSON.parse(storedData)
      mode.value = data.mode || 'insight'
      theme.value = data.theme || ''
      content.value = data.content || ''
      thoughtCount.value = data.thought_count || 0
      days.value = data.days || 0
      categories.value = data.categories || 0
      localStorage.removeItem('shareCardData')
      console.log('从localStorage加载卡片数据:', data)
    } catch (e) {
      console.error('解析卡片数据失败:', e)
    }
  }
  
  if (!content.value) {
    console.warn('卡片内容为空，这是旧的回顾记录')
    content.value = '此回顾是在更新前创建的，没有保存AI内容。\n\n请重新生成并保存回顾以查看完整内容。'
  }
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #f8f8fa;
  padding-bottom: 100px;
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

.card-container {
  padding: 20px;
  display: flex;
  justify-content: center;
}

.review-card {
  width: 100%;
  max-width: 500px;
  background: linear-gradient(135deg, #fdfcfb 0%, #f7f6f4 100%);
  border-radius: 20px;
  padding: 32px 24px;
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
}

.card-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
}

.meta-mode {
  color: #6366f1;
  font-weight: 600;
}

.meta-divider {
  color: #d1d5db;
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
  min-height: 100px;
}

.card-stats {
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 16px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #6366f1;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  margin-top: 4px;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: rgba(0, 0, 0, 0.1);
}

.actions {
  padding: 0 20px;
  display: flex;
  justify-content: center;
}

.action-btn {
  width: 100%;
  max-width: 500px;
  height: 52px;
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

  &:active {
    transform: scale(0.98);
  }
}
</style>
