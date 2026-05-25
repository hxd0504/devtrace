<template>
  <el-container class="app-layout">
    <el-aside width="200px">
      <div class="logo">DevTrace</div>
      <el-menu :default-active="route.path" router>
        <div class="nav-section-title">项目记忆中心</div>
        <el-menu-item index="/workspaces">项目空间</el-menu-item>
        <el-menu-item index="/knowledge">解决路径库</el-menu-item>
        <div class="nav-section-title">智能体调度中心</div>
        <el-menu-item index="/chat">调度台</el-menu-item>
        <el-menu-item index="/settings">设置</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <span>{{ authStore.user?.username }}</span>
        <el-button type="text" @click="handleLogout">退出</el-button>
      </el-header>
      <el-main>
        <slot />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.app-layout {
  height: 100vh;
}
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
}

.nav-section-title {
  padding: 12px 16px 4px;
  font-size: 11px;
  text-transform: uppercase;
  color: #909399;
  letter-spacing: 1px;
}
.el-header {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  border-bottom: 1px solid #eee;
}
</style>
