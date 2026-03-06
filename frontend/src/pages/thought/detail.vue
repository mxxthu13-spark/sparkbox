<template>
  <div class="page">
    <div v-if="thought" class="content">
      <!-- 顶部导航 -->
      <div class="nav-bar">
        <div class="nav-back" @click="goBack">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="20" height="20">
            <polyline points="15 18 9 12 15 6"/>
          </svg>
        </div>
        <span class="nav-title">想法详情</span>
        <div class="nav-edit" @click="goEdit">编辑</div>
      </div>

      <!-- 分类和时间 -->
      <div class="meta-section">
        <div v-if="thought.category" class="category-badge" :style="{ background: hexToLight(thought.category.color), color: thought.category.color }">
          {{ thought.category.icon }} {{ thought.category.name }}
        </div>
        <span class="time-text">{{ formatFullTime(thought.created_at) }}</span>
      </div>

      <!-- 内容 -->
      <div class="thought-content">
        {{ thought.content }}
      </div>

      <!-- 心情 -->
      <div v-if="thought.mood" class="mood-section">
        <span class="mood-icon">{{ thought.mood }}</span>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <button class="action-btn edit-btn" @click="goEdit">编辑</button>
        <button class="action-btn delete-btn" @click="handleDelete">删除</button>
      </div>
    </div>

    <div v-else class="loading">
      <span>加载中...</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../../utils/api'

const route = useRoute()
const router = useRouter()

const thought = ref(null)
const thoughtId = route.query.id

async function loadThought() {
  try {
    thought.value = await api.thoughts.get(thoughtId)
  } catch {
    uni.showToast({ title: '加载失败', icon: 'none' })
    router.back()
  }
}

function goBack() {
  router.back()
}

function goEdit() {
  router.push(`/capture?edit_id=${thoughtId}`)
}

async function handleDelete() {
  if (!window.confirm('确定要删除这条想法吗？')) {
    return
  }
  
  try {
    await api.thoughts.delete(thoughtId)
    uni.showToast({ title: '已删除', icon: 'none' })
    setTimeout(() => router.push('/home'), 800)
  } catch (e) {
    uni.showToast({ title: e.message || '删除失败', icon: 'none' })
  }
}

function formatFullTime(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日 ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

function hexToLight(hex) {
  try {
    const r = parseInt(hex.slice(1, 3), 16)
    const g = parseInt(hex.slice(3, 5), 16)
    const b = parseInt(hex.slice(5, 7), 16)
    return `rgba(${r},${g},${b},0.12)`
  } catch {
    return '#f0f0ff'
  }
}

onMounted(() => {
  if (!thoughtId) {
    router.back()
    return
  }
  loadThought()
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #fff;
}

.content {
  padding: 0 0 40px;
}

.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid #f3f4f6;
  position: sticky;
  top: 0;
  background: #fff;
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

.nav-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.nav-edit {
  padding: 7px 16px;
  background: #6366f1;
  color: #fff;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  
  &:active {
    opacity: 0.85;
  }
}

.meta-section {
  padding: 20px 20px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #f9fafb;
}

.category-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

.time-text {
  font-size: 13px;
  color: #9ca3af;
}

.thought-content {
  padding: 24px 20px;
  font-size: 17px;
  line-height: 1.8;
  color: #111827;
  white-space: pre-wrap;
}

.mood-section {
  padding: 0 20px 20px;
  display: flex;
  justify-content: center;
}

.mood-icon {
  font-size: 32px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  padding: 0 20px 40px;
}

.action-btn {
  flex: 1;
  height: 44px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;

  &:active {
    transform: scale(0.98);
  }
}

.edit-btn {
  background: #6366f1;
  color: #fff;

  &:hover {
    opacity: 0.9;
  }
}

.delete-btn {
  background: #fff;
  color: #ef4444;
  border: 1.5px solid #ef4444;

  &:hover {
    background: #fef2f2;
  }
}

.loading {
  display: flex;
  justify-content: center;
  padding: 100px 0;
  color: #9ca3af;
  font-size: 15px;
}
</style>
