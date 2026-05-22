<template>
  <div class="chat-view">
    <!-- 左侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">DevTrace</div>
        <el-button :icon="Plus" circle size="small" @click="createConversation" />
      </div>

      <div class="sidebar-nav">
        <div
          class="nav-item"
          :class="{ active: route.name === 'ChatHome' || route.name === 'ChatDetail' }"
          @click="router.push('/chat')"
        >
          <el-icon><ChatDotRound /></el-icon>
          <span>对话</span>
        </div>
        <div
          class="nav-item"
          :class="{ active: route.name === 'Knowledge' }"
          @click="router.push('/knowledge')"
        >
          <el-icon><Collection /></el-icon>
          <span>知识库</span>
        </div>
        <div
          class="nav-item"
          :class="{ active: route.path.startsWith('/workspaces') }"
          @click="router.push('/workspaces')"
        >
          <el-icon><FolderOpened /></el-icon>
          <span>项目空间</span>
        </div>
        <div
          class="nav-item"
          :class="{ active: route.name === 'Settings' }"
          @click="router.push('/settings')"
        >
          <el-icon><Setting /></el-icon>
          <span>设置</span>
        </div>
      </div>

      <!-- 项目列表 -->
      <ProjectList />

      <!-- 问题列表 -->
      <IssueList v-if="currentWorkspaceId" :workspace-id="currentWorkspaceId" />

      <!-- AI 标签面板 -->
      <AITagPanel v-if="currentWorkspaceId" :workspace-id="currentWorkspaceId" />

      <div class="sidebar-footer">
        <div class="user-info">
          <span>{{ authStore.user?.username }}</span>
          <el-button type="text" size="small" @click="handleLogout">退出</el-button>
        </div>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ChatDotRound, Collection, FolderOpened, Setting, Plus } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import ProjectList from '@/components/sidebar/ProjectList.vue'
import IssueList from '@/components/sidebar/IssueList.vue'
import AITagPanel from '@/components/dispatch/AITagPanel.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const currentWorkspaceId = computed(() => {
  // 从当前对话或项目空间获取 workspaceId
  return 1 // 默认工作空间
})

const createConversation = () => {
  router.push('/chat')
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.chat-view {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 280px;
  background: #1e1e2e;
  color: #cdd6f4;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  overflow-y: auto;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  border-bottom: 1px solid #313244;
}

.logo {
  font-size: 18px;
  font-weight: bold;
  color: #cba6f7;
}

.sidebar-nav {
  padding: 8px 0;
  border-bottom: 1px solid #313244;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  cursor: pointer;
  transition: background 0.2s;
  font-size: 14px;
}

.nav-item:hover {
  background: #313244;
}

.nav-item.active {
  background: #45475a;
  color: #cba6f7;
}

.sidebar-footer {
  margin-top: auto;
  padding: 12px 16px;
  border-top: 1px solid #313244;
}

.user-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
}

.main-content {
  flex: 1;
  min-width: 0;
  background: #f5f7fa;
}
</style>
