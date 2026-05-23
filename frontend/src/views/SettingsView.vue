<template>
  <V2Layout>
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
  </V2Layout>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import V2Layout from '@/layouts/V2Layout.vue'

const authStore = useAuthStore()

const defaultAITool = ref(localStorage.getItem('settings.defaultAITool') || 'Claude Code')
const autoDispatch = ref(localStorage.getItem('settings.autoDispatch') !== 'false')
const autoExtract = ref(localStorage.getItem('settings.autoExtract') !== 'false')

watch(defaultAITool, (v) => localStorage.setItem('settings.defaultAITool', v))
watch(autoDispatch, (v) => localStorage.setItem('settings.autoDispatch', String(v)))
watch(autoExtract, (v) => localStorage.setItem('settings.autoExtract', String(v)))
</script>

<style scoped>
.settings-page {
  padding: 24px;
  max-width: 800px;
}

.settings-page h2 {
  margin: 0 0 20px 0;
}
</style>
