<template>
  <AppLayout>
    <router-view v-slot="{ Component, route }">
      <transition :name="route.meta.transition || 'fade'" mode="out-in">
        <component :is="Component" :key="route.path" />
      </transition>
    </router-view>
  </AppLayout>
</template>

<script setup>
import { onMounted } from 'vue'
import AppLayout from './components/AppLayout.vue'
import { useUserStore } from './store/user'
import { useThoughtsStore } from './store/thoughts'

const userStore = useUserStore()
const thoughtsStore = useThoughtsStore()

onMounted(async () => {
  if (userStore.isLoggedIn) {
    await userStore.fetchUserInfo()
    await thoughtsStore.fetchCategories()
  }
})
</script>

<style lang="scss">
@use './uni.scss';

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  -webkit-tap-highlight-color: transparent;
}

html, body {
  height: 100%;
  overflow-x: hidden;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  background: #f8f8fa;
  max-width: 480px;
  margin: 0 auto;
  min-height: 100vh;
  position: relative;
}

#app {
  min-height: 100vh;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 通用按钮点击态 */
[class*="-btn"], [class*="btn-"] {
  cursor: pointer;
  user-select: none;
  &:active {
    opacity: 0.8;
  }
}
</style>
