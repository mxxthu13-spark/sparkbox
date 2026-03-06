<template>
  <div class="page">
    <h1>时间解析测试</h1>
    
    <div class="section">
      <h2>测试数据</h2>
      <div class="test-item">
        <label>输入时间字符串：</label>
        <input v-model="testTime" type="text" placeholder="2026-03-06T10:00:00" />
      </div>
      <button @click="runTest">测试解析</button>
    </div>
    
    <div v-if="result" class="section">
      <h2>解析结果</h2>
      <div class="result-item">
        <strong>原始字符串：</strong> {{ result.original }}
      </div>
      <div class="result-item">
        <strong>处理后字符串：</strong> {{ result.processed }}
      </div>
      <div class="result-item">
        <strong>正则匹配：</strong> {{ result.match ? '成功' : '失败' }}
      </div>
      <div class="result-item">
        <strong>解析后时间：</strong> {{ result.parsed }}
      </div>
      <div class="result-item">
        <strong>当前时间：</strong> {{ result.now }}
      </div>
      <div class="result-item">
        <strong>时间差（毫秒）：</strong> {{ result.diff }}
      </div>
      <div class="result-item">
        <strong>时间差（小时）：</strong> {{ result.diffHours }}
      </div>
      <div class="result-item">
        <strong>显示文本：</strong> {{ result.display }}
      </div>
    </div>
    
    <div class="section">
      <h2>从后端获取最新想法</h2>
      <button @click="fetchLatest">获取最新想法</button>
      <div v-if="latestThought" class="result-item">
        <strong>内容：</strong> {{ latestThought.content }}
      </div>
      <div v-if="latestThought" class="result-item">
        <strong>created_at：</strong> {{ latestThought.created_at }}
      </div>
      <div v-if="latestThought" class="result-item">
        <strong>显示时间：</strong> {{ formatTime(latestThought.created_at) }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '../../utils/api'

const testTime = ref('2026-03-06T10:00:00')
const result = ref(null)
const latestThought = ref(null)

function formatTime(ts) {
  if (!ts) return ''
  
  // 强制当作本地时间处理
  let timeStr = String(ts).replace(' ', 'T')
  
  // 移除任何时区标记
  timeStr = timeStr.replace('Z', '').replace(/[+-]\d{2}:\d{2}$/, '')
  
  // 手动解析为本地时间
  const match = timeStr.match(/^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})/)
  if (!match) return timeStr
  
  const d = new Date(
    parseInt(match[1]), // year
    parseInt(match[2]) - 1, // month (0-indexed)
    parseInt(match[3]), // day
    parseInt(match[4]), // hour
    parseInt(match[5]), // minute
    parseInt(match[6])  // second
  )
  
  const now = new Date()
  const diff = now - d
  
  if (diff < 0) return `${d.getMonth() + 1}/${d.getDate()}`
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 86400000 * 2) return '昨天'
  return `${d.getMonth() + 1}/${d.getDate()}`
}

function runTest() {
  const ts = testTime.value
  
  // 强制当作本地时间处理
  let timeStr = String(ts).replace(' ', 'T')
  
  // 移除任何时区标记
  timeStr = timeStr.replace('Z', '').replace(/[+-]\d{2}:\d{2}$/, '')
  
  // 手动解析为本地时间
  const match = timeStr.match(/^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})/)
  
  if (!match) {
    result.value = {
      original: ts,
      processed: timeStr,
      match: false,
      error: '正则匹配失败'
    }
    return
  }
  
  const d = new Date(
    parseInt(match[1]), // year
    parseInt(match[2]) - 1, // month (0-indexed)
    parseInt(match[3]), // day
    parseInt(match[4]), // hour
    parseInt(match[5]), // minute
    parseInt(match[6])  // second
  )
  
  const now = new Date()
  const diff = now - d
  
  result.value = {
    original: ts,
    processed: timeStr,
    match: true,
    parsed: d.toString(),
    now: now.toString(),
    diff: diff,
    diffHours: (diff / 3600000).toFixed(2),
    display: formatTime(ts)
  }
}

async function fetchLatest() {
  try {
    const res = await api.thoughts.list({ page: 1, page_size: 1 })
    if (res.items && res.items.length > 0) {
      latestThought.value = res.items[0]
      console.log('最新想法:', res.items[0])
    } else {
      uni.showToast({ title: '没有想法', icon: 'none' })
    }
  } catch (e) {
    uni.showToast({ title: e.message || '获取失败', icon: 'none' })
  }
}
</script>

<style lang="scss" scoped>
.page {
  padding: 20px;
  background: #f9fafb;
  min-height: 100vh;
}

h1 {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 20px;
}

h2 {
  font-size: 18px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 12px;
}

.section {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
}

.test-item {
  margin-bottom: 12px;
  
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
  }
}

button {
  width: 100%;
  height: 44px;
  background: #6366f1;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  
  &:active {
    opacity: 0.8;
  }
}

.result-item {
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
  margin-bottom: 8px;
  font-size: 14px;
  color: #374151;
  word-break: break-all;
  
  strong {
    color: #111827;
    display: block;
    margin-bottom: 4px;
  }
}
</style>
