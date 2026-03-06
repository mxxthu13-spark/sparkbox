<template>
  <div class="page">
    <!-- 顶部标题栏 -->
    <div class="nav-bar">
      <div class="nav-back" @click="handleCancel">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="20" height="20">
          <polyline points="15 18 9 12 15 6"/>
        </svg>
      </div>
      <span class="nav-title">{{ isEdit ? '编辑想法' : '记录想法' }}</span>
      <div class="nav-save" :class="{ disabled: !content.trim() }" @click="handleSave">
        <span v-if="!saving">{{ isEdit ? '保存' : '记录 ⚡' }}</span>
        <span v-else>保存中...</span>
      </div>
    </div>

    <div class="editor-container">
      <!-- 分类标签在输入框内 -->
      <div class="category-tags">
        <div
          v-for="cat in categories"
          :key="cat.id"
          :class="['cat-tag', selectedCategoryId === cat.id && 'active']"
          :style="selectedCategoryId === cat.id ? { background: cat.color, borderColor: cat.color, color: '#fff' } : {}"
          @click="toggleCategory(cat.id)"
        >
          <span>{{ cat.icon }} {{ cat.name }}</span>
        </div>
      </div>

      <!-- 输入区域 -->
      <textarea
        ref="textareaRef"
        v-model="content"
        class="textarea"
        :placeholder="randomPlaceholder"
        maxlength="2000"
        autofocus
      />
      
      <div class="editor-footer">
        <div class="left-tools">
          <span class="char-count">{{ content.length }}/2000</span>
          <button class="emoji-trigger" @click="showEmojiPicker = !showEmojiPicker">😊</button>
        </div>
        
        <!-- 心情选择 -->
        <div class="mood-selector">
          <div
            v-for="m in moods"
            :key="m.emoji"
            :class="['mood-btn', selectedMood === m.emoji && 'active']"
            @click="toggleMood(m.emoji)"
            :title="m.label"
          >
            {{ m.emoji }}
          </div>
        </div>
      </div>

      <!-- 表情选择器 -->
      <div v-if="showEmojiPicker" class="emoji-picker">
        <div class="emoji-grid">
          <span
            v-for="emoji in commonEmojis"
            :key="emoji"
            class="emoji-item"
            @click="insertEmoji(emoji)"
          >
            {{ emoji }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThoughtsStore } from '../../store/thoughts'
import { api } from '../../utils/api'

const route = useRoute()
const router = useRouter()
const thoughtsStore = useThoughtsStore()

const content = ref('')
const selectedCategoryId = ref(null)
const selectedMood = ref(null)
const saving = ref(false)
const textareaRef = ref(null)
const showEmojiPicker = ref(false)

const editId = route.query.edit_id
const isEdit = !!editId

const categories = computed(() => thoughtsStore.categories)

const placeholders = [
  '一个念头闪过，先记下来...',
  '此刻你在想什么？',
  '有什么想法别让它溜走...',
  '今天有什么新发现？',
  '把这个灵感留住...',
]
const randomPlaceholder = placeholders[Math.floor(Math.random() * placeholders.length)]

const commonEmojis = [
  '😊', '😂', '🥰', '😍', '🤗', '😘', '😋', '😎',
  '🤔', '😌', '😴', '🥱', '😪', '😔', '😢', '😭',
  '😤', '😠', '😡', '🤬', '😱', '😨', '😰', '😥',
  '🤯', '😳', '🥺', '😬', '🙄', '😏', '😶', '😐',
  '💪', '👍', '👎', '👏', '🙏', '🤝', '✌️', '🤞',
  '❤️', '💔', '💕', '💖', '💗', '💙', '💚', '💛',
  '⭐', '✨', '💫', '🌟', '🔥', '💥', '💯', '✅',
]

const moods = [
  { emoji: '✨', label: '激动' },
  { emoji: '😊', label: '开心' },
  { emoji: '🤔', label: '思考' },
  { emoji: '😌', label: '平静' },
  { emoji: '😔', label: '低落' },
]

function toggleCategory(id) {
  selectedCategoryId.value = selectedCategoryId.value === id ? null : id
}

function toggleMood(emoji) {
  selectedMood.value = selectedMood.value === emoji ? null : emoji
}

function insertEmoji(emoji) {
  const textarea = textareaRef.value
  if (!textarea) {
    content.value += emoji
    showEmojiPicker.value = false
    return
  }
  
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const text = content.value
  
  content.value = text.substring(0, start) + emoji + text.substring(end)
  
  // 关闭表情选择器
  showEmojiPicker.value = false
  
  // 恢复焦点并设置光标位置
  setTimeout(() => {
    textarea.focus()
    const newPos = start + emoji.length
    textarea.setSelectionRange(newPos, newPos)
  }, 0)
}

async function handleSave() {
  if (!content.value.trim() || saving.value) return
  saving.value = true
  try {
    if (isEdit) {
      await thoughtsStore.updateThought(editId, {
        content: content.value.trim(),
        category_id: selectedCategoryId.value,
        mood: selectedMood.value,
      })
      uni.showToast({ title: '已更新 ✓', icon: 'none', duration: 1200 })
    } else {
      await thoughtsStore.addThought({
        content: content.value.trim(),
        category_id: selectedCategoryId.value,
        mood: selectedMood.value,
      })
      uni.showToast({ title: '已记录 ⚡', icon: 'none', duration: 1200 })
    }
    setTimeout(() => router.back(), 800)
  } catch (e) {
    uni.showToast({ title: e.message || '保存失败', icon: 'none' })
  } finally {
    saving.value = false
  }
}

function handleCancel() {
  if (content.value.trim()) {
    if (window.confirm('当前内容尚未保存，确认放弃？')) {
      router.back()
    }
  } else {
    router.back()
  }
}

onMounted(async () => {
  if (!categories.value.length) {
    await thoughtsStore.fetchCategories()
  }

  // 编辑模式：从 store 或 API 加载已有数据
  if (isEdit) {
    try {
      const existing = thoughtsStore.list.find((t) => t.id === editId)
        || await api.thoughts.get(editId)
      content.value = existing.content
      selectedCategoryId.value = existing.category_id
      selectedMood.value = existing.mood || null
    } catch {
      uni.showToast({ title: '加载失败', icon: 'none' })
      router.back()
    }
  }
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #fff;
  display: flex;
  flex-direction: column;
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
  &:active { background: #f3f4f6; }
}

.nav-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.nav-save {
  padding: 7px 16px;
  background: #6366f1;
  color: #fff;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  &:active { opacity: 0.85; }
  &.disabled {
    background: #e5e7eb;
    color: #9ca3af;
    pointer-events: none;
  }
}

.editor-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 16px;
}

.category-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.cat-tag {
  display: inline-flex;
  align-items: center;
  padding: 6px 14px;
  border-radius: 20px;
  border: 1.5px solid #e5e7eb;
  background: #f9fafb;
  font-size: 13px;
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

.textarea {
  flex: 1;
  width: 100%;
  font-size: 17px;
  line-height: 1.75;
  color: #111827;
  border: none;
  outline: none;
  resize: none;
  font-family: inherit;
  background: transparent;
  min-height: 200px;

  &::placeholder {
    color: #d1d5db;
  }
}

.editor-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
  margin-top: 12px;
}

.left-tools {
  display: flex;
  align-items: center;
  gap: 12px;
}

.char-count {
  font-size: 12px;
  color: #d1d5db;
}

.emoji-trigger {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  border: none;
  background: #f3f4f6;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: #e5e7eb;
  }

  &:active {
    transform: scale(0.95);
  }
}

.emoji-picker {
  margin-top: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 12px;
  max-height: 200px;
  overflow-y: auto;
}

.emoji-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 8px;
}

.emoji-item {
  font-size: 24px;
  cursor: pointer;
  text-align: center;
  padding: 4px;
  border-radius: 6px;
  transition: all 0.2s;

  &:hover {
    background: #e5e7eb;
    transform: scale(1.2);
  }

  &:active {
    transform: scale(1.1);
  }
}

.mood-selector {
  display: flex;
  gap: 8px;
}

.mood-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1.5px solid transparent;
  
  &:hover {
    background: #f9fafb;
  }
  
  &.active {
    background: #f5f3ff;
    border-color: #6366f1;
  }
}
</style>
