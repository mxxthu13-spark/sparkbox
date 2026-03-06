/**
 * uni-app API 兼容层，让各页面无需修改即可在 H5 运行
 */
import router from '../router'

function parseUrl(url) {
  const [path, query] = url.split('?')
  const params = {}
  if (query) {
    query.split('&').forEach((pair) => {
      const [k, v] = pair.split('=')
      if (k) params[k] = v
    })
  }
  return { path, params }
}

function toRoute(url) {
  // 把 uni-app 风格的 /pages/xxx/index 转为 vue-router 路径
  const map = {
    '/pages/home/index': '/home',
    '/pages/login/index': '/login',
    '/pages/capture/index': '/capture',
    '/pages/thought/detail': '/thought/detail',
    '/pages/review/index': '/review',
    '/pages/review/detail': '/review/detail',
    '/pages/card/index': '/card',
    '/pages/card/create': '/card/create',
  }
  const { path, params } = parseUrl(url)
  const route = map[path] || path
  return { path: route, query: params }
}

const uni = {
  navigateTo({ url }) {
    const { path, query } = toRoute(url)
    router.push({ path, query })
  },
  redirectTo({ url }) {
    const { path, query } = toRoute(url)
    router.replace({ path, query })
  },
  reLaunch({ url }) {
    const { path, query } = toRoute(url)
    router.replace({ path, query })
  },
  switchTab({ url }) {
    const { path, query } = toRoute(url)
    router.push({ path, query })
  },
  navigateBack({ delta = 1 } = {}) {
    router.go(-delta)
  },

  request({ url, method = 'GET', data, header = {}, success, fail }) {
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...header,
      },
    }
    
    if (data && (method === 'POST' || method === 'PUT')) {
      options.body = JSON.stringify(data)
    }

    fetch(url, options)
      .then(async (response) => {
        const contentType = response.headers.get('content-type')
        let responseData
        if (contentType && contentType.includes('application/json')) {
          responseData = await response.json()
        } else {
          responseData = await response.text()
        }
        
        success?.({
          statusCode: response.status,
          data: responseData,
          header: Object.fromEntries(response.headers.entries()),
        })
      })
      .catch((error) => {
        fail?.({ errMsg: error.message })
      })
  },

  showToast({ title, icon = 'none', duration = 1500 }) {
    // 简单的 toast 实现
    const el = document.createElement('div')
    el.textContent = title
    el.style.cssText = `
      position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
      background: rgba(0,0,0,0.7); color: #fff; padding: 12px 20px;
      border-radius: 8px; font-size: 14px; z-index: 9999;
      pointer-events: none; white-space: nowrap;
    `
    document.body.appendChild(el)
    setTimeout(() => el.remove(), duration)
  },

  showModal({ title, content, confirmText = '确定', cancelText = '取消', success }) {
    const result = window.confirm(`${title}\n\n${content}`)
    success?.({ confirm: result, cancel: !result })
  },

  showLoading({ title }) {
    uni.showToast({ title, duration: 30000 })
  },

  hideLoading() {},

  setClipboardData({ data, success }) {
    navigator.clipboard?.writeText(data).then(() => success?.())
  },

  getStorageSync(key) {
    try { return JSON.parse(localStorage.getItem(key)) } catch { return localStorage.getItem(key) || '' }
  },

  setStorageSync(key, value) {
    localStorage.setItem(key, typeof value === 'string' ? value : JSON.stringify(value))
  },

  removeStorageSync(key) {
    localStorage.removeItem(key)
  },

  saveImageToPhotosAlbum({ filePath, success, fail }) {
    // H5 用下载链接代替
    try {
      const a = document.createElement('a')
      a.href = filePath
      a.download = 'sparkbox-card.png'
      a.click()
      success?.()
    } catch (e) {
      fail?.({ errMsg: e.message })
    }
  },
}

// 挂载到 window，让各组件内直接用
window.uni = uni

// getCurrentPages 兼容
window.getCurrentPages = () => {
  const route = router.currentRoute.value
  return [{ options: route.query }]
}

export default uni
