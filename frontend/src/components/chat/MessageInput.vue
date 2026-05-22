<template>
  <div class="message-input">
    <div class="input-wrapper">
      <el-input
        v-model="content"
        type="textarea"
        :rows="2"
        :placeholder="disabled ? '请先选择或创建对话...' : '输入消息... (Enter 发送，Shift+Enter 换行)'"
        :disabled="disabled"
        resize="none"
        @keydown="handleKeydown"
      />
      <div class="input-actions">
        <el-tooltip content="导入对话">
          <el-button :icon="Upload" circle size="small" @click="$emit('import')" />
        </el-tooltip>
        <el-button
          type="primary"
          :icon="Promotion"
          :loading="loading"
          :disabled="disabled || !content.trim()"
          @click="send"
        >
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Promotion, Upload } from '@element-plus/icons-vue'

defineProps<{
  disabled?: boolean
  loading?: boolean
}>()

const emit = defineEmits<{
  send: [content: string]
  import: []
}>()

const content = ref('')

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    send()
  }
}

const send = () => {
  const text = content.value.trim()
  if (!text) return
  emit('send', text)
  content.value = ''
}
</script>

<style scoped>
.message-input {
  padding: 12px 20px;
  background: #fff;
  border-top: 1px solid #ebeef5;
}

.input-wrapper {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.input-wrapper :deep(.el-textarea__inner) {
  border-radius: 8px;
  padding: 8px 12px;
}

.input-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}
</style>
