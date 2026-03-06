// 开发环境走本地代理，生产环境改为实际域名
const BASE_URL = process.env.NODE_ENV === 'development'
  ? '/api/v1'
  : 'https://your-api-domain.com/api/v1'

function getToken() {
  return uni.getStorageSync('access_token') || ''
}

function request(method, path, data = null) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}${path}`,
      method,
      data,
      header: {
        'Content-Type': 'application/json',
        Authorization: getToken() ? `Bearer ${getToken()}` : '',
      },
      success(res) {
        if (res.statusCode === 401) {
          uni.removeStorageSync('access_token')
          uni.reLaunch({ url: '/pages/login/index' })
          reject(new Error('未登录'))
          return
        }
        if (res.statusCode >= 400) {
          reject(new Error(res.data?.detail || '请求失败'))
          return
        }
        resolve(res.data)
      },
      fail(err) {
        reject(new Error(err.errMsg || '网络错误'))
      },
    })
  })
}

export const api = {
  // 认证
  auth: {
    register: (data) => request('POST', '/auth/register', data),
    login: (data) => request('POST', '/auth/login', data),
    getMe: () => request('GET', '/auth/me'),
    updateProfile: (data) => request('PUT', '/auth/me', data),
  },

  // 分类
  categories: {
    list: () => request('GET', '/categories/'),
    create: (data) => request('POST', '/categories/', data),
    update: (id, data) => request('PUT', `/categories/${id}`, data),
    delete: (id) => request('DELETE', `/categories/${id}`),
  },

  // 想法
  thoughts: {
    create: (data) => request('POST', '/thoughts/', data),
    list: (params) => {
      const query = new URLSearchParams()
      if (params) {
        Object.entries(params).forEach(([k, v]) => {
          if (v !== undefined && v !== null && v !== '') query.append(k, v)
        })
      }
      return request('GET', `/thoughts/?${query}`)
    },
    get: (id) => request('GET', `/thoughts/${id}`),
    update: (id, data) => request('PUT', `/thoughts/${id}`, data),
    delete: (id) => request('DELETE', `/thoughts/${id}`),
    stats: () => request('GET', '/thoughts/stats/summary'),
  },

  // 回顾
  reviews: {
    generate: (data) => request('POST', '/reviews/generate', data),
    list: (params) => {
      const query = new URLSearchParams()
      if (params) Object.entries(params).forEach(([k, v]) => v && query.append(k, v))
      return request('GET', `/reviews/?${query}`)
    },
    getLatestWeek: () => request('GET', '/reviews/latest-week'),
    get: (id) => request('GET', `/reviews/${id}`),
    update: (id, data) => request('PUT', `/reviews/${id}`, data),
  },

  // 卡片
  cards: {
    templates: () => request('GET', '/cards/templates'),
    create: (data) => request('POST', '/cards/', data),
    list: (params) => {
      const query = new URLSearchParams()
      if (params) Object.entries(params).forEach(([k, v]) => v && query.append(k, v))
      return request('GET', `/cards/?${query}`)
    },
    delete: (id) => request('DELETE', `/cards/${id}`),
  },

  // AI
  ai: {
    refine: (data) => request('POST', '/ai/refine', data),
    summarize: (data) => request('POST', '/ai/summarize', data),
    monthlyReport: (data) => request('POST', '/ai/monthly-report', data),
  },
}

export default api
