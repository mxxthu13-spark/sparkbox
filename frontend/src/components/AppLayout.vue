<template>
  <div class="app-layout">
    <div class="page-content" :class="{ 'with-nav': hasNav }">
      <slot />
    </div>
    <BottomNav v-if="hasNav" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import BottomNav from './BottomNav.vue'

const route = useRoute()

// 这几个路由显示底部导航栏
const NAV_ROUTES = ['/home', '/review', '/settings']
const hasNav = computed(() => NAV_ROUTES.includes(route.path))
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  position: relative;
}

.page-content.with-nav {
  padding-bottom: calc(60px + env(safe-area-inset-bottom));
}
</style>
