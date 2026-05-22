<template>
  <div class="message-bubble" :class="[`role-${message.role}`, `type-${message.message_type}`]">
    <div class="avatar" v-if="message.role !== 'user'">
      <el-icon v-if="message.role === 'assistant'" :size="20"><Monitor /></el-icon>
      <el-icon v-else :size="20"><InfoFilled /></el-icon>
    </div>

    <div class="bubble-content">
      <div class="bubble-header">
        <span class="role-name">{{ roleLabel }}</span>
        <span class="time">{{ formatTime(message.created_at) }}</span>
      </div>
      <div class="bubble-body" v-html="formattedContent" />
      <div v-if="message.message_type === 'knowledge_extract'" class="knowledge-badge">
        <el-icon><Collection /></el-icon>
        <span>已提取到知识库</span>
      </div>
      <div v-if="message.message_type === 'execution_result'" class="execution-badge">
        <el-icon><Finished /></el-icon>
        <span>执行完成</span>
      </div>
    </div>

    <div class="avatar" v-if="message.role === 'user'">
      <el-icon :size="20"><User /></el-icon>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Monitor, InfoFilled, User, Collection, Finished } from '@element-plus/icons-vue'
import type { Message } from '@/types/conversation'

const props = defineProps<{ message: Message }>()

const roleLabel = computed(() => {
  const map: Record<string, string> = {
    user: '你',
    assistant: 'AI 助手',
    system: '系统',
  }
  return map[props.message.role] || props.message.role
})

const formattedContent = computed(() => {
  // 简单的 markdown 转换：换行 → <br>，代码块处理
  return props.message.content
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
})

const formatTime = (time: string) => {
  return new Date(time).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.message-bubble {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  max-width: 80%;
}

.role-user {
  margin-left: auto;
  flex-direction: row-reverse;
}

.role-system {
  margin: 0 auto;
  max-width: 60%;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.role-user .avatar {
  background: #409eff;
  color: #fff;
}

.role-assistant .avatar {
  background: #e4e7ed;
  color: #606266;
}

.role-system .avatar {
  background: #fdf6ec;
  color: #e6a23c;
}

.bubble-content {
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
}

.role-user .bubble-content {
  background: #409eff;
  color: #fff;
}

.role-assistant .bubble-content {
  background: #f4f4f5;
  color: #303133;
}

.role-system .bubble-content {
  background: #fdf6ec;
  color: #909399;
  text-align: center;
  font-size: 13px;
}

.type-execution_result .bubble-content {
  border-left: 3px solid #67c23a;
}

.type-knowledge_extract .bubble-content {
  border-left: 3px solid #9b59b6;
}

.bubble-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
  font-size: 12px;
}

.role-name {
  font-weight: 600;
}

.role-user .bubble-header {
  color: rgba(255, 255, 255, 0.8);
}

.role-assistant .bubble-header,
.role-system .bubble-header {
  color: #909399;
}

.time {
  margin-left: 12px;
}

.bubble-body :deep(code) {
  background: rgba(0, 0, 0, 0.06);
  padding: 1px 4px;
  border-radius: 3px;
  font-family: monospace;
  font-size: 13px;
}

.role-user .bubble-body :deep(code) {
  background: rgba(255, 255, 255, 0.2);
}

.knowledge-badge,
.execution-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.knowledge-badge {
  background: #f0e6ff;
  color: #9b59b6;
}

.execution-badge {
  background: #e1f3d8;
  color: #67c23a;
}
</style>
