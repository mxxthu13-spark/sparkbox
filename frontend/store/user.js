import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '../utils/api'

export const useUserStore = defineStore('user', () => {
  const token = ref(uni.getStorageSync('access_token') || '')
  const userInfo = ref(null)

  const isLoggedIn = computed(() => !!token.value)

  function setToken(newToken) {
    token.value = newToken
    uni.setStorageSync('access_token', newToken)
  }

  function clearToken() {
    token.value = ''
    userInfo.value = null
    uni.removeStorageSync('access_token')
  }

  async function fetchUserInfo() {
    try {
      const data = await api.auth.getMe()
      userInfo.value = data
    } catch {
      clearToken()
    }
  }

  async function login(phone, password) {
    const data = await api.auth.login({ phone, password })
    setToken(data.access_token)
    userInfo.value = {
      user_id: data.user_id,
      nickname: data.nickname,
      avatar_url: data.avatar_url,
    }
    return data
  }

  async function register(phone, password, nickname) {
    const data = await api.auth.register({ phone, password, nickname })
    setToken(data.access_token)
    userInfo.value = {
      user_id: data.user_id,
      nickname: data.nickname,
      avatar_url: data.avatar_url,
    }
    return data
  }

  function logout() {
    clearToken()
    uni.reLaunch({ url: '/pages/login/index' })
  }

  return { token, userInfo, isLoggedIn, login, register, logout, fetchUserInfo }
})
