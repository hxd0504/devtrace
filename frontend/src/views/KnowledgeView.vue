<template>
  <div class="chat-view">
    <!-- 左侧边栏（复用） -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">DevTrace</div>
      </div>
      <div class="sidebar-nav">
        <div class="nav-item" @click="router.push('/chat')">
          <el-icon><ChatDotRound /></el-icon>
          <span>对话</span>
        </div>
        <div class="nav-item active">
          <el-icon><Collection /></el-icon>
          <span>知识库</span>
        </div>
        <div class="nav-item" @click="router.push('/workspaces')">
          <el-icon><FolderOpened /></el-icon>
          <span>项目空间</span>
        </div>
        <div class="nav-item" @click="router.push('/settings')">
          <el-icon><Setting /></el-icon>
          <span>设置</span>
        </div>
      </div>
      <ProjectList />
      <div class="sidebar-footer">
        <div class="user-info">
          <span>{{ authStore.user?.username }}</span>
          <el-button type="text" size="small" @click="handleLogout">退出</el-button>
        </div>
      </div>
    </aside>

    <!-- 知识库主内容 -->
    <main class="main-content">
      <KnowledgePanel :workspace-id="currentWorkspaceId" />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ChatDotRound, Collection, FolderOpened, Setting } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import ProjectList from '@/components/sidebar/ProjectList.vue'
import KnowledgePanel from '@/components/knowledge/KnowledgePanel.vue'

const router = useRouter()
const authStore = useAuthStore()
const currentWorkspaceId = 1

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
  overflow-y: auto;
}
</style>
