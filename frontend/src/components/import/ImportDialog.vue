<template>
  <el-dialog
    :model-value="modelValue"
    title="导入对话"
    width="600px"
    @update:model-value="$emit('update:modelValue', $event)"
    @close="reset"
  >
    <el-tabs v-model="activeTab">
      <!-- ChatGPT 导入 -->
      <el-tab-pane label="ChatGPT 导入" name="chatgpt">
        <el-form label-width="80px">
          <el-form-item label="对话链接">
            <el-input v-model="chatgptForm.url" placeholder="粘贴 ChatGPT 分享链接（选填）" />
          </el-form-item>
          <el-form-item label="对话内容">
            <el-input
              v-model="chatgptForm.content"
              type="textarea"
              :rows="8"
              placeholder="粘贴 ChatGPT 对话内容..."
            />
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 手动导入 -->
      <el-tab-pane label="手动导入" name="manual">
        <el-form label-width="80px">
          <el-form-item label="标题">
            <el-input v-model="manualForm.title" placeholder="输入对话标题" />
          </el-form-item>
          <el-form-item label="内容">
            <el-input
              v-model="manualForm.content"
              type="textarea"
              :rows="8"
              placeholder="粘贴对话内容..."
            />
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>

    <!-- 预览 -->
    <ImportPreview v-if="previewData" :data="previewData" />

    <template #footer>
      <el-button @click="handlePreview">预览</el-button>
      <el-button type="primary" :loading="loading" @click="handleImport">导入</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import ImportPreview from './ImportPreview.vue'
import { importApi } from '@/api/import'

defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  imported: [conversationId: number]
}>()

const activeTab = ref('chatgpt')
const loading = ref(false)
const previewData = ref<{ title: string; content: string; source: string } | null>(null)

const chatgptForm = reactive({ url: '', content: '' })
const manualForm = reactive({ title: '', content: '' })

const handlePreview = () => {
  if (activeTab.value === 'chatgpt') {
    if (!chatgptForm.content.trim()) {
      ElMessage.warning('请输入对话内容')
      return
    }
    previewData.value = {
      title: 'ChatGPT 对话',
      content: chatgptForm.content,
      source: 'chatgpt_web',
    }
  } else {
    if (!manualForm.title.trim() || !manualForm.content.trim()) {
      ElMessage.warning('请填写标题和内容')
      return
    }
    previewData.value = {
      title: manualForm.title,
      content: manualForm.content,
      source: 'manual_import',
    }
  }
}

const handleImport = async () => {
  loading.value = true
  try {
    let conv
    if (activeTab.value === 'chatgpt') {
      conv = await importApi.importChatGPT({
        url: chatgptForm.url || undefined,
        content: chatgptForm.content,
      })
    } else {
      conv = await importApi.importManual({
        title: manualForm.title,
        content: manualForm.content,
      })
    }
    ElMessage.success('导入成功')
    emit('imported', conv.id)
    emit('update:modelValue', false)
    reset()
  } catch {
    ElMessage.error('导入失败')
  } finally {
    loading.value = false
  }
}

const reset = () => {
  chatgptForm.url = ''
  chatgptForm.content = ''
  manualForm.title = ''
  manualForm.content = ''
  previewData.value = null
  activeTab.value = 'chatgpt'
}
</script>
