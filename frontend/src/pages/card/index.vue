<template>
  <div class="page">
    <div class="header">
      <span class="title">我的卡片</span>
      <div class="new-btn" @tap="goCreate">+ 新建</div>
    </div>

    <div v-if="cards.length === 0 && !loading" class="empty-state">
      <span class="empty-icon">🃏</span>
      <span class="empty-title">还没有卡片</span>
      <span class="empty-sub">从想法页面生成你的第一张精美卡片</span>
      <div class="empty-btn" @tap="goCreate">创建第一张卡片</div>
    </div>

    <div class="cards-grid">
      <div
        v-for="card in cards"
        :key="card.id"
        class="card-item"
        :style="{ background: getTemplateColor(card.template_id) }"
        @tap="previewCard(card)"
        @longpress="showCardActions(card)"
      >
        <span class="card-content" :style="{ color: getTemplateTextColor(card.template_id) }">
          {{ card.content.slice(0, 60) }}{{ card.content.length > 60 ? '...' : '' }}
        </span>
        <div class="card-footer">
          <span class="card-tpl-name" :style="{ color: getTemplateTextColor(card.template_id), opacity: 0.6 }">{{ getTemplateName(card.template_id) }}</span>
          <span class="card-date" :style="{ color: getTemplateTextColor(card.template_id), opacity: 0.5 }">{{ formatDate(card.created_at) }}</span>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-tip">加载中...</div>

    <div v-if="actionCard" class="action-mask" @tap="actionCard = null">
      <div class="action-sheet" @tap.stop>
        <div class="action-item" @tap="exportCard">导出图片</div>
        <div class="action-item danger" @tap="deleteCard">删除卡片</div>
        <div class="action-cancel" @tap="actionCard = null">取消</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../../utils/api'

const cards = ref([])
const loading = ref(false)
const actionCard = ref(null)

const TEMPLATE_COLORS = {
  minimal: { bg: '#ffffff', text: '#1a1a1a', name: '极简白' },
  night: { bg: '#1a1a2e', text: '#e8e8ff', name: '深夜黑' },
  forest: { bg: '#1a3a2a', text: '#c8f0d8', name: '林间绿' },
  warm: { bg: '#fff7ed', text: '#7c2d12', name: '暖橙' },
  note: { bg: '#fefce8', text: '#713f12', name: '手账风' },
}

function getTemplateColor(id) {
  return TEMPLATE_COLORS[id]?.bg || '#f9fafb'
}
function getTemplateTextColor(id) {
  return TEMPLATE_COLORS[id]?.text || '#111827'
}
function getTemplateName(id) {
  return TEMPLATE_COLORS[id]?.name || id
}

function formatDate(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  return `${d.getMonth() + 1}/${d.getDate()}`
}

function goCreate() {
  uni.navigateTo({ url: '/pages/card/create' })
}

function previewCard(card) {
  const content = encodeURIComponent(card.content)
  uni.navigateTo({
    url: `/pages/card/create?content=${content}&template=${card.template_id}`,
  })
}

function showCardActions(card) {
  actionCard.value = card
}

function exportCard() {
  if (!actionCard.value) return
  const card = actionCard.value
  actionCard.value = null
  const content = encodeURIComponent(card.content)
  uni.navigateTo({
    url: `/pages/card/create?content=${content}&template=${card.template_id}`,
  })
}

async function deleteCard() {
  if (!actionCard.value) return
  const id = actionCard.value.id
  actionCard.value = null
  uni.showModal({
    title: '删除卡片',
    content: '确定要删除这张卡片吗？',
    success: async (res) => {
      if (res.confirm) {
        await api.cards.delete(id)
        cards.value = cards.value.filter((c) => c.id !== id)
        uni.showToast({ title: '已删除', icon: 'none' })
      }
    },
  })
}

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.cards.list({ page_size: 50 })
    cards.value = res.items || []
  } finally {
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #f8f8fa;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx 32rpx;
  background: #fff;
}

.title {
  font-size: 36rpx;
  font-weight: 700;
  color: #111827;
}

.new-btn {
  background: #6366f1;
  color: #fff;
  border-radius: 100rpx;
  padding: 12rpx 28rpx;
  font-size: 26rpx;
}

.cards-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
  padding: 24rpx;
}

.card-item {
  width: calc(50% - 10rpx);
  aspect-ratio: 3 / 4;
  border-radius: 20rpx;
  padding: 24rpx;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.card-content {
  font-size: 26rpx;
  line-height: 1.7;
  flex: 1;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 16rpx;
}

.card-tpl-name,
.card-date {
  font-size: 20rpx;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 120rpx 60rpx;
}

.empty-icon {
  font-size: 100rpx;
  margin-bottom: 24rpx;
}

.empty-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #374151;
  margin-bottom: 12rpx;
}

.empty-sub {
  font-size: 26rpx;
  color: #9ca3af;
  margin-bottom: 48rpx;
  text-align: center;
}

.empty-btn {
  width: 360rpx;
  height: 88rpx;
  line-height: 88rpx;
  font-size: 30rpx;
  background: #6366f1;
  color: #fff;
  border-radius: 16rpx;
  text-align: center;
}

.loading-tip {
  text-align: center;
  padding: 32rpx;
  font-size: 26rpx;
  color: #9ca3af;
}

.action-mask {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: flex-end;
  z-index: 100;
}

.action-sheet {
  width: 100%;
  background: #fff;
  border-radius: 32rpx 32rpx 0 0;
  padding: 16rpx 0;
  padding-bottom: constant(safe-area-inset-bottom);
  padding-bottom: env(safe-area-inset-bottom);
}

.action-item {
  padding: 36rpx 48rpx;
  font-size: 32rpx;
  color: #111827;
  border-bottom: 1rpx solid #f3f4f6;
}

.action-item.danger {
  color: #ef4444;
}

.action-cancel {
  padding: 36rpx 48rpx;
  font-size: 32rpx;
  color: #9ca3af;
  text-align: center;
  margin-top: 8rpx;
}
</style>

