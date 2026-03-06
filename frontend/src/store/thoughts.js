import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '../utils/api'

export const useThoughtsStore = defineStore('thoughts', () => {
  const list = ref([])
  const total = ref(0)
  const categories = ref([])
  const currentPage = ref(1)
  const loading = ref(false)
  const hasMore = ref(true)

  async function fetchCategories() {
    categories.value = await api.categories.list()
  }

  async function createCategory(data) {
    const category = await api.categories.create(data)
    categories.value.push(category)
    return category
  }

  async function updateCategory(id, data) {
    const updated = await api.categories.update(id, data)
    const idx = categories.value.findIndex((c) => c.id === id)
    if (idx !== -1) categories.value[idx] = updated
    return updated
  }

  async function deleteCategory(id) {
    await api.categories.delete(id)
    const idx = categories.value.findIndex((c) => c.id === id)
    if (idx !== -1) categories.value.splice(idx, 1)
  }

  async function fetchThoughts(params = {}, reset = false) {
    if (loading.value) return
    loading.value = true
    try {
      if (reset) {
        currentPage.value = 1
        list.value = []
        hasMore.value = true
      }
      const res = await api.thoughts.list({ ...params, page: currentPage.value, page_size: 20 })
      if (reset) {
        list.value = res.items
      } else {
        list.value.push(...res.items)
      }
      total.value = res.total
      hasMore.value = list.value.length < res.total
      currentPage.value++
    } finally {
      loading.value = false
    }
  }

  async function loadMore(params = {}) {
    if (!hasMore.value || loading.value) return
    await fetchThoughts(params)
  }

  async function addThought(data) {
    const thought = await api.thoughts.create(data)
    list.value.unshift(thought)
    total.value++
    return thought
  }

  async function updateThought(id, data) {
    const updated = await api.thoughts.update(id, data)
    const idx = list.value.findIndex((t) => t.id === id)
    if (idx !== -1) list.value[idx] = updated
    return updated
  }

  async function deleteThought(id) {
    await api.thoughts.delete(id)
    const idx = list.value.findIndex((t) => t.id === id)
    if (idx !== -1) {
      list.value.splice(idx, 1)
      total.value--
    }
  }

  function getCategoryById(id) {
    return categories.value.find((c) => c.id === id) || null
  }

  return {
    list,
    total,
    categories,
    loading,
    hasMore,
    fetchCategories,
    createCategory,
    updateCategory,
    deleteCategory,
    fetchThoughts,
    loadMore,
    addThought,
    updateThought,
    deleteThought,
    getCategoryById,
  }
})
