<template>
  <div class="container">
    <div class="hero">
      <div class="logo">⚡</div>
      <h1 class="app-name">闪念盒子</h1>
      <p class="app-slogan">捕捉每一道灵感的闪光</p>
    </div>

    <div class="form-card">
      <div class="tabs">
        <span :class="['tab', mode === 'login' && 'active']" @click="mode = 'login'">登录</span>
        <span :class="['tab', mode === 'register' && 'active']" @click="mode = 'register'">注册</span>
      </div>

      <div class="form">
        <div class="input-wrap">
          <label class="label">手机号</label>
          <input
            v-model="phone"
            class="input"
            type="tel"
            maxlength="11"
            placeholder="请输入手机号"
          />
        </div>

        <div v-if="mode === 'register'" class="input-wrap">
          <label class="label">昵称</label>
          <input
            v-model="nickname"
            class="input"
            type="text"
            maxlength="20"
            placeholder="你想叫什么？"
          />
        </div>

        <div class="input-wrap">
          <label class="label">密码</label>
          <div class="password-field">
            <input
              v-model="password"
              class="input"
              :type="showPwd ? 'text' : 'password'"
              maxlength="30"
              placeholder="请输入密码"
            />
            <span class="pwd-toggle" @click="showPwd = !showPwd">{{ showPwd ? '隐藏' : '显示' }}</span>
          </div>
        </div>

        <div v-if="error" class="error-msg">{{ error }}</div>

        <button class="submit-btn" @click="handleSubmit" :disabled="loading">
          <span v-if="!loading">{{ mode === 'login' ? '登录' : '注册' }}</span>
          <span v-else>处理中...</span>
        </button>
      </div>
    </div>

    <p class="hint">私密记录，数据仅属于你</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '../../store/user'
import { useThoughtsStore } from '../../store/thoughts'

const userStore = useUserStore()
const thoughtsStore = useThoughtsStore()

const mode = ref('login')
const phone = ref('')
const password = ref('')
const nickname = ref('')
const showPwd = ref(false)
const loading = ref(false)
const error = ref('')

async function handleSubmit() {
  error.value = ''
  if (!phone.value || phone.value.length !== 11) {
    error.value = '请输入正确的手机号'
    return
  }
  if (!password.value || password.value.length < 6) {
    error.value = '密码至少 6 位'
    return
  }

  loading.value = true
  try {
    if (mode.value === 'login') {
      await userStore.login(phone.value, password.value)
    } else {
      await userStore.register(phone.value, password.value, nickname.value || '闪念用户')
    }
    await thoughtsStore.fetchCategories()
    uni.switchTab({ url: '/pages/home/index' })
  } catch (e) {
    error.value = e.message || '操作失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: linear-gradient(160deg, #f0f0ff 0%, #f8f8fa 60%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
}

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 40px;
}

.logo {
  font-size: 64px;
  margin-bottom: 16px;
}

.app-name {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  letter-spacing: 2px;
  margin: 0 0 8px;
}

.app-slogan {
  font-size: 14px;
  color: #9ca3af;
  margin: 0;
}

.form-card {
  width: 100%;
  max-width: 400px;
  background: #fff;
  border-radius: 20px;
  padding: 32px 24px;
  box-shadow: 0 4px 24px rgba(99, 102, 241, 0.08);
}

.tabs {
  display: flex;
  margin-bottom: 32px;
  border-bottom: 2px solid #f3f4f6;
}

.tab {
  flex: 1;
  text-align: center;
  font-size: 16px;
  color: #9ca3af;
  padding-bottom: 12px;
  cursor: pointer;
  transition: all 0.2s;

  &.active {
    color: #6366f1;
    font-weight: 600;
    border-bottom: 3px solid #6366f1;
    margin-bottom: -2px;
  }
}

.input-wrap {
  margin-bottom: 20px;
}

.label {
  display: block;
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
  font-weight: 500;
}

.input {
  width: 100%;
  height: 48px;
  border: 1.5px solid #e5e7eb;
  border-radius: 12px;
  padding: 0 16px;
  font-size: 15px;
  background: #f9fafb;
  box-sizing: border-box;
  transition: all 0.2s;

  &:focus {
    outline: none;
    border-color: #6366f1;
    background: #fff;
  }

  &::placeholder {
    color: #d1d5db;
  }
}

.password-field {
  position: relative;
}

.pwd-toggle {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 13px;
  color: #6366f1;
  cursor: pointer;
  user-select: none;
}

.error-msg {
  color: #ef4444;
  font-size: 13px;
  margin-bottom: 16px;
  text-align: center;
  padding: 8px;
  background: #fef2f2;
  border-radius: 8px;
}

.submit-btn {
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
  margin-top: 8px;

  &:hover {
    opacity: 0.9;
  }

  &:active {
    transform: scale(0.98);
  }

  &:disabled {
    background: #9ca3af;
    cursor: not-allowed;
  }
}

.hint {
  margin-top: 24px;
  font-size: 13px;
  color: #9ca3af;
}
</style>


