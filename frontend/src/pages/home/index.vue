<template>
  <div class="page">
    <!-- 顶部栏 -->
    <div class="header">
      <div class="logo-section">
        <svg class="logo-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span class="app-title">闪念盒子</span>
      </div>
      <div class="greeting-section">
        <span class="greeting-text">{{ greeting }}，{{ nickname }}</span>
      </div>
      <div class="header-actions">
        <div class="search-btn" @click="showSearch = !showSearch">🔍</div>
        <div class="stats-badge" @click="goStats">
          <span>{{ total }}</span>
          <span class="stats-unit"> 条</span>
        </div>
      </div>
    </div>

    <!-- 搜索栏 -->
    <div v-if="showSearch" class="search-bar">
      <input
        v-model="searchKeyword"
        class="search-input"
        placeholder="搜索想法..."
        @input="onSearchInput"
        @confirm="doSearch"
      />
      <span v-if="searchKeyword" class="search-clear" @tap="clearSearch">×</span>
    </div>

    <!-- 分类筛选 -->
    <div class="filter-scroll"  style="overflow-x:auto;white-space:nowrap">
      <div class="filter-list">
        <div
          :class="['filter-item', !activeCategory && 'active']"
          @click="setCategory(null)"
        >全部</div>
        <div
          v-for="cat in categories"
          :key="cat.id"
          :class="['filter-item', activeCategory === cat.id && 'active']"
          :style="activeCategory === cat.id ? { background: cat.color, borderColor: cat.color, color: '#fff' } : {}"
          @click="setCategory(cat.id)"
        >
          <span>{{ cat.icon }} {{ cat.name }}</span>
        </div>
      </div>
    </div>

    <!-- 时间轴列表 -->
    <div
      class="list-scroll"
       style="overflow-y:auto"
      @scrolltolower="loadMore"
    >
      <div v-if="groupedThoughts.length === 0 && !loading" class="empty-state">
        <span class="empty-icon">✨</span>
        <span class="empty-title">还没有想法</span>
        <span class="empty-sub">把一个想法放在这里</span>
      </div>

      <div v-for="group in groupedThoughts" :key="group.date" class="date-group">
        <div class="date-header">
          <div class="date-dot" />
          <span class="date-text">{{ group.label }}</span>
          <span class="date-count">{{ group.items.length }} 条</span>
        </div>
        <div class="date-items">
          <ThoughtCard
            v-for="t in group.items"
            :key="t.id"
            :thought="t"
            compact
            @click="openDetail(t)"
          />
        </div>
      </div>

      <div v-if="loading" class="loading-tip">
        <span>加载中...</span>
      </div>
      <div v-if="!hasMore && groupedThoughts.length > 0" class="end-tip">
        <span>— 已经到底啦 —</span>
      </div>
    </div>

    <!-- 悬浮写作按钮 -->
    <div class="fab" @click="goCapture">
      <span class="fab-icon">⚡</span>
    </div>

    <!-- 操作菜单 (长按) -->
    <div v-if="actionTarget" class="action-mask" @click="actionTarget = null">
      <div class="action-sheet" @click.stop>
        <div class="action-item" @click="pinThought">
          <span>{{ actionTarget.is_pinned ? '取消置顶' : '置顶' }}</span>
        </div>
        <div class="action-item" @click="goCreateCard">
          <span>生成卡片</span>
        </div>
        <div class="action-item ai-item" @click="goAIRefine">
          <span>✦ AI 润色</span>
        </div>
        <div class="action-item danger" @click="confirmDelete">
          <span>删除</span>
        </div>
        <div class="action-cancel" @click="actionTarget = null">
          <span>取消</span>
        </div>
      </div>
    </div>

    <!-- 底部导航 -->
    <BottomNav />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import ThoughtCard from '../../components/ThoughtCard.vue'
import BottomNav from '../../components/BottomNav.vue'
import { useThoughtsStore } from '../../store/thoughts'
import { useUserStore } from '../../store/user'

const thoughtsStore = useThoughtsStore()
const userStore = useUserStore()

const showSearch = ref(false)
const searchKeyword = ref('')
const activeCategory = ref(null)
const actionTarget = ref(null)

const categories = computed(() => thoughtsStore.categories)
const loading = computed(() => thoughtsStore.loading)
const hasMore = computed(() => thoughtsStore.hasMore)
const total = computed(() => thoughtsStore.total)
const nickname = computed(() => userStore.userInfo?.nickname || '朋友')

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 6) return '深夜好'
  if (h < 12) return '早上好'
  if (h < 14) return '中午好'
  if (h < 18) return '下午好'
  return '晚上好'
})

const groupedThoughts = computed(() => {
  const groups = {}
  for (const t of thoughtsStore.list) {
    const d = new Date(t.created_at)
    const key = `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`
    if (!groups[key]) {
      groups[key] = { date: key, label: formatDate(d), items: [] }
    }
    groups[key].items.push(t)
  }
  return Object.values(groups).sort((a, b) => b.date.localeCompare(a.date))
})

function formatDate(d) {
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const target = new Date(d.getFullYear(), d.getMonth(), d.getDate())
  const diff = today - target
  if (diff === 0) return '今天'
  if (diff === 86400000) return '昨天'
  if (diff < 86400000 * 7) return `${Math.floor(diff / 86400000)} 天前`
  return `${d.getMonth() + 1}月${d.getDate()}日`
}

let searchTimer = null
function onSearchInput() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(doSearch, 500)
}

function doSearch() {
  loadThoughts(true)
}

function clearSearch() {
  searchKeyword.value = ''
  loadThoughts(true)
}

function setCategory(id) {
  activeCategory.value = id
  loadThoughts(true)
}

async function loadThoughts(reset = false) {
  const params = {}
  if (activeCategory.value) params.category_id = activeCategory.value
  if (searchKeyword.value) params.search = searchKeyword.value
  await thoughtsStore.fetchThoughts(params, reset)
}

async function loadMore() {
  const params = {}
  if (activeCategory.value) params.category_id = activeCategory.value
  if (searchKeyword.value) params.search = searchKeyword.value
  await thoughtsStore.loadMore(params)
}

function goCapture() {
  uni.navigateTo({ url: '/pages/capture/index' })
}

function openDetail(thought) {
  uni.navigateTo({ url: `/pages/thought/detail?id=${thought.id}` })
}

function showActions(thought) {
  actionTarget.value = thought
}

async function pinThought() {
  if (!actionTarget.value) return
  await thoughtsStore.updateThought(actionTarget.value.id, {
    is_pinned: !actionTarget.value.is_pinned,
  })
  actionTarget.value = null
  uni.showToast({ title: '已更新', icon: 'none' })
}

function goCreateCard() {
  if (!actionTarget.value) return
  const id = actionTarget.value.id
  const content = encodeURIComponent(actionTarget.value.content)
  actionTarget.value = null
  uni.navigateTo({ url: `/pages/card/create?thought_id=${id}&content=${content}` })
}

function goAIRefine() {
  if (!actionTarget.value) return
  const id = actionTarget.value.id
  actionTarget.value = null
  uni.navigateTo({ url: `/pages/thought/detail?id=${id}&ai=1` })
}

function confirmDelete() {
  if (!actionTarget.value) return
  const id = actionTarget.value.id
  actionTarget.value = null
  uni.showModal({
    title: '删除想法',
    content: '确定要删除这条想法吗？',
    success: async (res) => {
      if (res.confirm) {
        await thoughtsStore.deleteThought(id)
        uni.showToast({ title: '已删除', icon: 'none' })
      }
    },
  })
}

function goStats() {}

onMounted(async () => {
  if (!userStore.isLoggedIn) {
    uni.reLaunch({ url: '/pages/login/index' })
    return
  }
  await thoughtsStore.fetchCategories()
  await loadThoughts(true)
})

</script>

<style lang="scss" scoped>
.page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f8f8fa;
}

.header {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 24px 20px 16px;
  background: #fff;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 32px;
  height: 32px;
  color: #6366f1;
  flex-shrink: 0;
}

.app-title {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  letter-spacing: 1px;
}

.greeting-section {
  padding-left: 48px;
}

.greeting-text {
  font-size: 14px;
  color: #9ca3af;
}

.header-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  margin-top: -40px;
}

.search-btn {
  font-size: 20px;
  cursor: pointer;
  padding: 8px;
}

.stats-badge {
  background: #f0f0ff;
  border-radius: 100px;
  padding: 6px 16px;
  cursor: pointer;
}

.stats-badge span {
  font-size: 14px;
  font-weight: 600;
  color: #6366f1;
}

.stats-unit {
  font-size: 12px;
  color: #9ca3af;
}

.search-bar {
  background: #fff;
  padding: 8px 20px 12px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-input {
  flex: 1;
  height: 40px;
  background: #f3f4f6;
  border-radius: 20px;
  padding: 0 16px;
  font-size: 14px;
  border: none;
  outline: none;
}

.search-input::placeholder {
  color: #d1d5db;
}

.search-clear {
  font-size: 24px;
  color: #9ca3af;
  line-height: 1;
  cursor: pointer;
}

.filter-scroll {
  background: #fff;
  padding: 0 16px;
  border-bottom: 1px solid #f3f4f6;
}

.filter-list {
  display: inline-flex;
  gap: 10px;
  padding: 12px 0;
}

.filter-item {
  white-space: nowrap;
  padding: 6px 16px;
  border-radius: 20px;
  border: 1px solid #e5e7eb;
  font-size: 13px;
  color: #6b7280;
  background: #f9fafb;
  cursor: pointer;
  transition: all 0.2s;

  &.active {
    background: #6366f1;
    border-color: #6366f1;
    color: #fff;
    font-weight: 500;
  }
}

.list-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.date-group {
  margin-bottom: 8px;
}

.date-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.date-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #6366f1;
  flex-shrink: 0;
}

.date-text {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
}

.date-count {
  font-size: 12px;
  color: #9ca3af;
}

.date-items {
  padding-left: 16px;
  border-left: 2px solid #e5e7eb;
  margin-left: 3px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80px 0;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-title {
  font-size: 18px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.empty-sub {
  font-size: 14px;
  color: #9ca3af;
}

.loading-tip,
.end-tip {
  text-align: center;
  padding: 20px;
  font-size: 13px;
  color: #9ca3af;
}

.fab {
  position: fixed;
  right: 24px;
  bottom: 80px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4);
  cursor: pointer;
  transition: transform 0.2s;
  z-index: 100;
}

.fab:active {
  transform: scale(0.95);
}

.fab-icon {
  font-size: 28px;
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
  border-radius: 16px 16px 0 0;
  padding: 8px 0;
  padding-bottom: env(safe-area-inset-bottom);
}

.action-item {
  padding: 16px 24px;
  font-size: 16px;
  color: #111827;
  border-bottom: 1px solid #f3f4f6;
  cursor: pointer;

  &.danger {
    color: #ef4444;
  }

  &.ai-item {
    color: #6366f1;
    font-weight: 500;
  }
}

.action-cancel {
  padding: 16px 24px;
  font-size: 16px;
  color: #9ca3af;
  text-align: center;
  margin-top: 4px;
  cursor: pointer;
}
</style>


