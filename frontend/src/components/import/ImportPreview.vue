<template>
  <div class="import-preview">
    <el-divider>预览</el-divider>
    <div class="preview-header">
      <span class="preview-title">{{ data.title }}</span>
      <el-tag size="small" :type="sourceType">{{ sourceLabel }}</el-tag>
    </div>
    <div class="preview-content">
      <pre>{{ truncatedContent }}</pre>
    </div>
    <div class="preview-meta">
      <span>内容长度: {{ data.content.length }} 字符</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  data: { title: string; content: string; source: string }
}>()

const sourceType = computed(() => {
  return props.data.source === 'chatgpt_web' ? 'success' : 'info'
})

const sourceLabel = computed(() => {
  const map: Record<string, string> = { chatgpt_web: 'ChatGPT', manual_import: '手动导入' }
  return map[props.data.source] || props.data.source
})

const truncatedContent = computed(() => {
  const max = 300
  if (props.data.content.length <= max) return props.data.content
  return props.data.content.slice(0, max) + '...'
})
</script>

<style scoped>
.import-preview {
  margin-top: 12px;
}

.preview-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.preview-title {
  font-weight: 600;
  font-size: 14px;
}

.preview-content {
  background: #f5f7fa;
  border-radius: 6px;
  padding: 12px;
  max-height: 200px;
  overflow-y: auto;
}

.preview-content pre {
  margin: 0;
  font-family: inherit;
  font-size: 13px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-all;
}

.preview-meta {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}
</style>
