<template>
  <div class="page">
    <!-- 内容编辑区 -->
    <div class="editor-section">
      <span class="section-label">卡片内容</span>
      <textarea
        v-model="cardContent"
        class="content-input"
        placeholder="输入想要展示在卡片上的内容..."
        :maxlength="300"
      />
      <span class="char-hint">{{ cardContent.length }}/300</span>

      <div v-if="showAiTools" class="ai-quote-input">
        <span class="ai-quote-label">✦ AI 金句（可选）</span>
        <input
          v-model="aiQuote"
          class="quote-input"
          placeholder="留空则不显示金句"
        />
      </div>
    </div>

    <!-- 模板选择 -->
    <div class="template-section">
      <span class="section-label">风格模板</span>
      <div class="template-scroll"  style="overflow-x:auto;white-space:nowrap">
        <div class="template-list">
          <div
            v-for="tpl in templates"
            :key="tpl.id"
            :class="['template-item', selectedTemplate === tpl.id && 'active']"
            :style="{ background: tpl.preview_color, borderColor: selectedTemplate === tpl.id ? '#6366f1' : 'transparent' }"
            @tap="selectTemplate(tpl.id)"
          >
            <span class="template-name" :style="{ color: tpl.text_color }">{{ tpl.name }}</span>
            <div v-if="selectedTemplate === tpl.id" class="template-check">✓</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Canvas 预览 -->
    <div class="preview-section">
      <span class="section-label">预览</span>
      <div class="canvas-wrap">
        <canvas
          id="cardCanvas"
          class="card-canvas"
          type="2d"
          :style="{ background: currentTemplate.preview_color }"
        />
        <div class="preview-overlay" :style="{ background: currentTemplate.preview_color }">
          <!-- 顶部装饰 -->
          <div class="preview-accent-bar" :style="{ background: previewAccentColor }" />
          <span class="preview-brand" :style="{ color: previewAccentColor }">⚡ 闪念盒子</span>
          <div class="preview-divider" :style="{ background: currentTemplate.text_color, opacity: 0.15 }" />

          <!-- 正文 -->
          <span class="preview-content" :style="{ color: currentTemplate.text_color }">{{ cardContent || '在这里预览卡片内容' }}</span>

          <!-- 金句 -->
          <div v-if="aiQuote" class="preview-quote" :style="{ background: previewAccentColor + '18' }">
            <span class="preview-quote-icon" :style="{ color: previewAccentColor }">✦</span>
            <span class="preview-quote-text" :style="{ color: previewAccentColor }">{{ aiQuote }}</span>
          </div>

          <!-- 底部 -->
          <div class="preview-footer">
            <div class="preview-divider-sm" :style="{ background: currentTemplate.text_color, opacity: 0.15 }" />
            <div class="preview-meta">
              <span :style="{ color: currentTemplate.text_color, opacity: 0.5 }">{{ todayStr }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部操作 -->
    <div class="bottom-actions safe-bottom">
      <div class="action-save-card" @tap="saveCard">
        <span v-if="!saving">保存卡片</span>
        <span v-else>保存中...</span>
      </div>
      <div class="action-export" @tap="exportImage">
        <span v-if="!exporting">导出图片</span>
        <span v-else>生成中...</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../../utils/api'
import { generateCard, downloadCard } from '../../utils/canvas'

const cardContent = ref('')
const aiQuote = ref('')
const selectedTemplate = ref('minimal')
const templates = ref([])
const saving = ref(false)
const exporting = ref(false)
const showAiTools = ref(true)

let thoughtId = null
let reviewId = null

const TEMPLATE_ACCENT_COLORS = {
  minimal: '#6366f1',
  night: '#818cf8',
  forest: '#34d399',
  warm: '#ea580c',
  note: '#d97706',
}

const currentTemplate = computed(() => {
  return templates.value.find((t) => t.id === selectedTemplate.value) || {
    preview_color: '#ffffff',
    text_color: '#111827',
  }
})

const previewAccentColor = computed(() => TEMPLATE_ACCENT_COLORS[selectedTemplate.value] || '#6366f1')

const todayStr = computed(() => {
  const d = new Date()
  return `${d.getFullYear()}/${d.getMonth() + 1}/${d.getDate()}`
})

function selectTemplate(id) {
  selectedTemplate.value = id
}

async function saveCard() {
  if (!cardContent.value.trim() || saving.value) return
  saving.value = true
  try {
    await api.cards.create({
      content: cardContent.value.trim(),
      template_id: selectedTemplate.value,
      thought_id: thoughtId || undefined,
      review_id: reviewId || undefined,
      card_config: { ai_quote: aiQuote.value },
    })
    uni.showToast({ title: '卡片已保存', icon: 'none' })
    setTimeout(() => uni.navigateBack(), 800)
  } catch (e) {
    uni.showToast({ title: e.message || '保存失败', icon: 'none' })
  } finally {
    saving.value = false
  }
}

async function exportImage() {
  if (!cardContent.value.trim() || exporting.value) return
  exporting.value = true
  try {
    const dataURL = await generateCard({
      content: cardContent.value,
      templateId: selectedTemplate.value,
      date: todayStr.value,
      author: '闪念盒子',
      quote: aiQuote.value,
    })
    downloadCard(dataURL)
    uni.showToast({ title: '图片已下载 ✓', icon: 'none' })
  } catch (e) {
    uni.showToast({ title: e.message || '图片生成失败', icon: 'none' })
  } finally {
    exporting.value = false
  }
}

const route = useRoute()

onMounted(async () => {
  const q = route.query
  if (q.thought_id) thoughtId = q.thought_id
  if (q.review_id) reviewId = q.review_id
  if (q.content) cardContent.value = decodeURIComponent(q.content)
  if (q.template) selectedTemplate.value = q.template

  const tpls = await api.cards.templates()
  templates.value = tpls
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #f8f8fa;
  padding-bottom: 160rpx;
}

.editor-section,
.template-section,
.preview-section {
  background: #fff;
  padding: 32rpx;
  margin-bottom: 16rpx;
}

.section-label {
  font-size: 24rpx;
  color: #9ca3af;
  font-weight: 500;
  display: block;
  margin-bottom: 16rpx;
}

.content-input {
  width: 100%;
  min-height: 160rpx;
  font-size: 30rpx;
  line-height: 1.7;
  color: #111827;
  box-sizing: border-box;
}

.ph {
  color: #d1d5db;
}

.char-hint {
  display: block;
  text-align: right;
  font-size: 22rpx;
  color: #d1d5db;
  margin-top: 8rpx;
}

.ai-quote-input {
  margin-top: 20rpx;
  padding-top: 20rpx;
  border-top: 1rpx solid #f3f4f6;
}

.ai-quote-label {
  font-size: 24rpx;
  color: #6366f1;
  display: block;
  margin-bottom: 12rpx;
}

.quote-input {
  height: 72rpx;
  width: 100%;
  border: 2rpx solid #ede9fe;
  border-radius: 12rpx;
  padding: 0 20rpx;
  font-size: 28rpx;
  background: #f5f3ff;
  box-sizing: border-box;
}

.template-scroll {
  white-space: nowrap;
}

.template-list {
  display: inline-flex;
  gap: 20rpx;
  padding: 4rpx 0;
}

.template-item {
  position: relative;
  width: 160rpx;
  height: 200rpx;
  border-radius: 16rpx;
  border: 4rpx solid transparent;
  display: flex;
  align-items: flex-end;
  padding: 20rpx;
  box-sizing: border-box;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.1);

  &.active {
    border-color: #6366f1;
  }
}

.template-name {
  font-size: 24rpx;
  font-weight: 500;
}

.template-check {
  position: absolute;
  top: 12rpx;
  right: 12rpx;
  width: 36rpx;
  height: 36rpx;
  border-radius: 50%;
  background: #6366f1;
  color: #fff;
  font-size: 22rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 卡片预览 */
.canvas-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 3/4;
  border-radius: 20rpx;
  overflow: hidden;
}

.card-canvas {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
}

.preview-overlay {
  position: absolute;
  inset: 0;
  padding: 40rpx;
  display: flex;
  flex-direction: column;
  border-radius: 20rpx;
  overflow: hidden;
}

.preview-accent-bar {
  height: 6rpx;
  border-radius: 100rpx;
  margin-bottom: 24rpx;
  width: 80rpx;
}

.preview-brand {
  font-size: 24rpx;
  font-weight: 600;
  margin-bottom: 20rpx;
}

.preview-divider {
  height: 1rpx;
  margin-bottom: 28rpx;
}

.preview-content {
  font-size: 30rpx;
  line-height: 1.8;
  flex: 1;
  overflow: hidden;
}

.preview-quote {
  display: flex;
  align-items: flex-start;
  gap: 12rpx;
  padding: 16rpx;
  border-radius: 12rpx;
  margin-top: 20rpx;
}

.preview-quote-icon {
  font-size: 22rpx;
  flex-shrink: 0;
}

.preview-quote-text {
  font-size: 24rpx;
  font-style: italic;
  line-height: 1.6;
}

.preview-footer {
  margin-top: 24rpx;
}

.preview-divider-sm {
  height: 1rpx;
  margin-bottom: 16rpx;
}

.preview-meta {
  font-size: 22rpx;
}

/* 底部操作 */
.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  border-top: 1rpx solid #f3f4f6;
  display: flex;
  gap: 24rpx;
  padding: 24rpx 32rpx;
}

.action-save-card {
  flex: 1;
  height: 88rpx;
  line-height: 88rpx;
  border-radius: 16rpx;
  text-align: center;
  font-size: 30rpx;
  font-weight: 500;
  background: #f0f0ff;
  color: #6366f1;
}

.action-export {
  flex: 2;
  height: 88rpx;
  line-height: 88rpx;
  border-radius: 16rpx;
  text-align: center;
  font-size: 30rpx;
  font-weight: 600;
  background: #6366f1;
  color: #fff;
}
</style>


