<template>
  <nav class="bottom-nav">
    <router-link to="/home" class="nav-item" active-class="active">
      <span class="nav-icon">⚡</span>
      <span class="nav-label">想法</span>
    </router-link>

    <router-link to="/review" class="nav-item" active-class="active">
      <span class="nav-icon">📊</span>
      <span class="nav-label">回顾</span>
    </router-link>

    <router-link to="/settings" class="nav-item" active-class="active">
      <span class="nav-icon">⚙️</span>
      <span class="nav-label">设置</span>
    </router-link>
  </nav>
</template>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 480px;
  background: #fff;
  border-top: 1px solid #f3f4f6;
  display: flex;
  padding-bottom: env(safe-area-inset-bottom);
  z-index: 50;
}

.nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 0 8px;
  color: #9ca3af;
  text-decoration: none;
  transition: color 0.15s;
  gap: 3px;
}

.nav-item.active {
  color: #6366f1;
}

.nav-icon {
  font-size: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-label {
  font-size: 11px;
  font-weight: 500;
}
</style>
