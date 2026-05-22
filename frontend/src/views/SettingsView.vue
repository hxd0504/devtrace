<template>
  <div class="chat-view">
    <!-- 左侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">DevTrace</div>
      </div>
      <div class="sidebar-nav">
        <div class="nav-item" @click="router.push('/chat')">
          <el-icon><ChatDotRound /></el-icon>
          <span>对话</span>
        </div>
        <div class="nav-item" @click="router.push('/knowledge')">
          <el-icon><Collection /></el-icon>
          <span>知识库</span>
        </div>
        <div class="nav-item" @click="router.push('/workspaces')">
          <el-icon><FolderOpened /></el-icon>
          <span>项目空间</span>
        </div>
        <div class="nav-item active">
          <el-icon><Setting /></el-icon>
          <span>设置</span>
        </div>
      </div>
      <div class="sidebar-footer">
        <div class="user-info">
          <span>{{ authStore.user?.username }}</span>
          <el-button type="text" size="small" @click="handleLogout">退出</el-button>
        </div>
      </div>
    </aside>

    <!-- 设置主内容 -->
    <main class="main-content">
      <div class="settings-page">
        <h2>设置</h2>
        <el-card>
          <template #header>
            <span>AI 工具配置</span>
          </template>
          <el-form label-width="120px">
            <el-form-item label="默认 AI 工具">
              <el-select v-model="defaultAITool" style="width: 300px">
                <el-option label="Claude Code" value="Claude Code" />
                <el-option label="Codex" value="Codex" />
                <el-option label="GPT" value="GPT" />
              </el-select>
            </el-form-item>
            <el-form-item label="自动调度">
              <el-switch v-model="autoDispatch" />
            </el-form-item>
            <el-form-item label="知识自动提取">
              <el-switch v-model="autoExtract" />
            </el-form-item>
          </el-form>
        </el-card>

        <el-card style="margin-top: 16px">
          <template #header>
            <span>用户信息</span>
          </template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="用户名">{{ authStore.user?.username }}</el-descriptions-item>
            <el-descriptions-item label="用户ID">{{ authStore.user?.id }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ChatDotRound, Collection, FolderOpened, Setting } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const defaultAITool = ref('Claude Code')
const autoDispatch = ref(true)
const autoExtract = ref(true)

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
}

.sidebar-header {
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

.settings-page {
  padding: 24px;
  max-width: 800px;
}

.settings-page h2 {
  margin: 0 0 20px 0;
}
</style>
