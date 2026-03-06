<template>
  <div class="page">
    <div class="header">
      <h1 class="title">设置</h1>
    </div>

    <div class="content">
      <!-- 账号管理 -->
      <div class="section">
        <div class="section-title">账号管理</div>
        <div class="setting-item" @click="showProfileModal = true">
          <span class="item-label">个人信息</span>
          <span class="item-value">{{ userInfo?.nickname }}</span>
          <span class="item-arrow">›</span>
        </div>
        <div class="setting-item" @click="handleLogout">
          <span class="item-label danger">退出登录</span>
        </div>
      </div>

      <!-- 自定义分类 -->
      <div class="section">
        <div class="section-title">
          <span>自定义分类</span>
          <span class="add-btn" @click="showAddCategory = true">+ 添加</span>
        </div>
        <div class="category-list">
          <div
            v-for="cat in categories"
            :key="cat.id"
            class="category-item"
          >
            <span class="cat-icon">{{ cat.icon }}</span>
            <span class="cat-name">{{ cat.name }}</span>
            <span class="cat-color" :style="{ background: cat.color }"></span>
            <div class="cat-actions">
              <span class="cat-action-btn" @click="editCategory(cat)">编辑</span>
              <span class="cat-action-btn delete" @click="deleteCategory(cat)">删除</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 回顾风格 -->
      <div class="section">
        <div class="section-title">回顾风格</div>
        <div class="setting-item" @click="setReviewStyle('summary')">
          <span class="item-label">摘要模式</span>
          <span v-if="reviewStyle === 'summary'" class="item-check">✓</span>
        </div>
        <div class="setting-item" @click="setReviewStyle('insight')">
          <span class="item-label">洞察模式</span>
          <span v-if="reviewStyle === 'insight'" class="item-check">✓</span>
        </div>
        <div class="setting-item" @click="setReviewStyle('soul')">
          <span class="item-label">灵魂模式</span>
          <span v-if="reviewStyle === 'soul'" class="item-check">✓</span>
        </div>
      </div>
    </div>

    <!-- 个人信息编辑弹窗 -->
    <div v-if="showProfileModal" class="modal-mask" @click="showProfileModal = false">
      <div class="modal-content" @click.stop>
        <h3 class="modal-title">个人信息</h3>
        <div class="form-group">
          <label>昵称</label>
          <input v-model="editNickname" placeholder="输入昵称" maxlength="20" />
        </div>
        <div class="modal-actions">
          <button class="btn-secondary" @click="showProfileModal = false">取消</button>
          <button class="btn-primary" @click="saveProfile">保存</button>
        </div>
      </div>
    </div>

    <!-- 添加分类弹窗 -->
    <div v-if="showAddCategory" class="modal-mask" @click="showAddCategory = false">
      <div class="modal-content" @click.stop>
        <h3 class="modal-title">添加分类</h3>
        <div class="form-group">
          <label>图标</label>
          <div class="icon-picker">
            <div
              v-for="icon in iconOptions"
              :key="icon"
              class="icon-option"
              :class="{ active: newCategory.icon === icon }"
              @click="newCategory.icon = icon"
            >
              {{ icon }}
            </div>
          </div>
        </div>
        <div class="form-group">
          <label>名称</label>
          <input v-model="newCategory.name" placeholder="分类名称" maxlength="10" />
        </div>
        <div class="form-group">
          <label>颜色</label>
          <div class="color-picker">
            <div
              v-for="color in colorOptions"
              :key="color"
              class="color-option"
              :class="{ active: newCategory.color === color }"
              :style="{ background: color }"
              @click="newCategory.color = color"
            ></div>
          </div>
        </div>
        <div class="modal-actions">
          <button class="btn-secondary" @click="showAddCategory = false">取消</button>
          <button class="btn-primary" @click="addCategory">确定</button>
        </div>
      </div>
    </div>

    <!-- 编辑分类弹窗 -->
    <div v-if="showEditCategory && editingCategory" class="modal-mask" @click="showEditCategory = false">
      <div class="modal-content" @click.stop>
        <h3 class="modal-title">编辑分类</h3>
        <div class="form-group">
          <label>图标</label>
          <div class="icon-picker">
            <div
              v-for="icon in iconOptions"
              :key="icon"
              class="icon-option"
              :class="{ active: editingCategory.icon === icon }"
              @click="editingCategory.icon = icon"
            >
              {{ icon }}
            </div>
          </div>
        </div>
        <div class="form-group">
          <label>名称</label>
          <input v-model="editingCategory.name" placeholder="分类名称" maxlength="10" />
        </div>
        <div class="form-group">
          <label>颜色</label>
          <div class="color-picker">
            <div
              v-for="color in colorOptions"
              :key="color"
              class="color-option"
              :class="{ active: editingCategory.color === color }"
              :style="{ background: color }"
              @click="editingCategory.color = color"
            ></div>
          </div>
        </div>
        <div class="modal-actions">
          <button class="btn-secondary" @click="showEditCategory = false">取消</button>
          <button class="btn-primary" @click="saveEditCategory">保存</button>
        </div>
      </div>
    </div>

    <!-- 底部导航 -->
    <BottomNav />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../../store/user'
import { useThoughtsStore } from '../../store/thoughts'
import BottomNav from '../../components/BottomNav.vue'

const userStore = useUserStore()
const thoughtsStore = useThoughtsStore()

const showProfileModal = ref(false)
const showAddCategory = ref(false)
const showEditCategory = ref(false)
const reviewStyle = ref(localStorage.getItem('reviewStyle') || 'insight')
const editNickname = ref('')

const newCategory = ref({
  icon: '📝',
  name: '',
  color: '#6366f1',
})

const editingCategory = ref(null)

const iconOptions = [
  '📝', '💡', '🎯', '💼', '📚', '🎨', '🏃', '🍔',
  '✈️', '💰', '❤️', '🎵', '🎮', '📱', '🏠', '🌟',
  '🔥', '⚡', '🌈', '🎁', '🔔', '📌', '🎓', '🏆',
]

const colorOptions = [
  '#6366f1', '#8b5cf6', '#ec4899', '#f43f5e',
  '#f59e0b', '#10b981', '#06b6d4', '#6b7280',
]

const userInfo = computed(() => userStore.userInfo)
const categories = computed(() => thoughtsStore.categories)

function setReviewStyle(style) {
  reviewStyle.value = style
  localStorage.setItem('reviewStyle', style)
  uni.showToast({ title: '已保存', icon: 'none' })
}

async function saveProfile() {
  if (!editNickname.value.trim()) {
    uni.showToast({ title: '请输入昵称', icon: 'none' })
    return
  }
  
  try {
    await userStore.updateProfile({ nickname: editNickname.value.trim() })
    uni.showToast({ title: '保存成功', icon: 'none' })
    showProfileModal.value = false
  } catch (e) {
    uni.showToast({ title: e.message || '保存失败', icon: 'none' })
  }
}

async function addCategory() {
  if (!newCategory.value.name) {
    uni.showToast({ title: '请输入分类名称', icon: 'none' })
    return
  }
  
  try {
    await thoughtsStore.createCategory(newCategory.value)
    uni.showToast({ title: '添加成功', icon: 'none' })
    showAddCategory.value = false
    newCategory.value = { icon: '📝', name: '', color: '#6366f1' }
  } catch (e) {
    uni.showToast({ title: e.message || '添加失败', icon: 'none' })
  }
}

function editCategory(cat) {
  editingCategory.value = { ...cat }
  showEditCategory.value = true
}

async function saveEditCategory() {
  if (!editingCategory.value.name) {
    uni.showToast({ title: '请输入分类名称', icon: 'none' })
    return
  }
  
  try {
    await thoughtsStore.updateCategory(editingCategory.value.id, {
      name: editingCategory.value.name,
      icon: editingCategory.value.icon,
      color: editingCategory.value.color,
    })
    uni.showToast({ title: '保存成功', icon: 'none' })
    showEditCategory.value = false
    editingCategory.value = null
  } catch (e) {
    uni.showToast({ title: e.message || '保存失败', icon: 'none' })
  }
}

async function deleteCategory(cat) {
  if (!window.confirm(`确定要删除分类"${cat.name}"吗？`)) {
    return
  }
  
  try {
    await thoughtsStore.deleteCategory(cat.id)
    uni.showToast({ title: '删除成功', icon: 'none' })
  } catch (e) {
    uni.showToast({ title: e.message || '删除失败', icon: 'none' })
  }
}

function handleLogout() {
  uni.showModal({
    title: '退出登录',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        userStore.logout()
      }
    },
  })
}

onMounted(async () => {
  await thoughtsStore.fetchCategories()
  editNickname.value = userInfo.value?.nickname || ''
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

.content {
  padding: 16px;
}

.section {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.add-btn {
  color: #6366f1;
  font-size: 14px;
  cursor: pointer;
}

.setting-item {
  display: flex;
  align-items: center;
  padding: 14px 0;
  border-bottom: 1px solid #f3f4f6;
  cursor: pointer;

  &:last-child {
    border-bottom: none;
  }
}

.item-label {
  flex: 1;
  font-size: 15px;
  color: #111827;

  &.danger {
    color: #ef4444;
  }
}

.item-value {
  font-size: 14px;
  color: #9ca3af;
  margin-right: 8px;
}

.item-arrow {
  font-size: 20px;
  color: #d1d5db;
}

.item-check {
  font-size: 18px;
  color: #6366f1;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.category-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
  transition: background 0.2s;

  &:hover {
    background: #f3f4f6;
  }
}

.cat-icon {
  font-size: 20px;
}

.cat-name {
  flex: 1;
  font-size: 15px;
  color: #111827;
}

.cat-color {
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.cat-actions {
  display: flex;
  gap: 8px;
}

.cat-action-btn {
  font-size: 13px;
  color: #6366f1;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s;

  &:hover {
    background: #f5f3ff;
  }

  &.delete {
    color: #ef4444;

    &:hover {
      background: #fef2f2;
    }
  }
}

.modal-mask {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-content {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  width: 90%;
  max-width: 400px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 20px;
}

.form-group {
  margin-bottom: 16px;

  label {
    display: block;
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 8px;
  }

  input {
    width: 100%;
    height: 44px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 0 12px;
    font-size: 15px;
    box-sizing: border-box;

    &:focus {
      outline: none;
      border-color: #6366f1;
    }
  }
}

.icon-picker {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 8px;
}

.icon-option {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  border-radius: 8px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
  background: #f9fafb;

  &:hover {
    background: #f3f4f6;
  }

  &.active {
    border-color: #6366f1;
    background: #f5f3ff;
  }
}

.color-picker {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.color-option {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  cursor: pointer;
  border: 3px solid transparent;
  transition: all 0.2s;

  &.active {
    border-color: #111827;
    transform: scale(1.1);
  }
}

.modal-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.btn-secondary,
.btn-primary {
  flex: 1;
  height: 44px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary {
  background: #f3f4f6;
  color: #6b7280;

  &:hover {
    background: #e5e7eb;
  }
}

.btn-primary {
  background: #6366f1;
  color: #fff;

  &:hover {
    background: #4f46e5;
  }
}
</style>
