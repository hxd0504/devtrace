<template>
  <el-dialog
    :model-value="true"
    title="AI 调度确认"
    width="600px"
    @close="$emit('close')"
  >
    <div v-if="loading" class="loading">
      <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      <p>正在分析任务并推荐 AI 工具...</p>
    </div>
    <template v-else-if="result">
      <div class="dispatch-result">
        <el-alert
          :title="`推荐工具：${result.recommended_tool}`"
          :description="result.reason"
          type="success"
          show-icon
          :closable="false"
        />

        <div class="detail-section">
          <h4>执行提示词</h4>
          <el-input
            v-model="result.execution_prompt"
            type="textarea"
            :rows="4"
            readonly
          />
        </div>

        <div class="detail-section">
          <h4>风险等级</h4>
          <el-tag :type="riskType(result.risk_level)" size="large">
            {{ riskLabel(result.risk_level) }}
          </el-tag>
        </div>

        <div class="detail-section" v-if="result.alternatives.length">
          <h4>备选方案</h4>
          <div v-for="alt in result.alternatives" :key="alt.tool" class="alt-item">
            <span class="alt-tool">{{ alt.tool }}</span>
            <span class="alt-reason">{{ alt.reason }}</span>
          </div>
        </div>
      </div>
    </template>

    <template #footer>
      <el-button @click="$emit('close')">取消</el-button>
      <el-button type="primary" @click="handleConfirm">
        <el-icon><Promotion /></el-icon>
        确认执行
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Loading, Promotion } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { dispatchApi } from '@/api/dispatch'
import type { DispatchResponse } from '@/types/dispatch'

const props = defineProps<{ taskId: number }>()
const emit = defineEmits<{ close: [] }>()

const loading = ref(true)
const result = ref<DispatchResponse | null>(null)

const riskType = (level: string) => {
  const map: Record<string, string> = { low: 'success', medium: 'warning', high: 'danger' }
  return map[level] || 'info'
}

const riskLabel = (level: string) => {
  const map: Record<string, string> = { low: '低风险', medium: '中风险', high: '高风险' }
  return map[level] || level
}

onMounted(async () => {
  try {
    result.value = await dispatchApi.dispatch({ task_id: props.taskId })
  } catch {
    ElMessage.error('调度分析失败')
  } finally {
    loading.value = false
  }
})

const handleConfirm = () => {
  ElMessage.success('已下发执行')
  emit('close')
}
</script>

<style scoped>
.loading {
  text-align: center;
  padding: 40px;
  color: #909399;
}

.dispatch-result {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-section h4 {
  margin: 0 0 8px;
  font-size: 14px;
  color: #303133;
}

.alt-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #ebeef5;
}

.alt-item:last-child {
  border-bottom: none;
}

.alt-tool {
  font-weight: 600;
  color: #409eff;
  min-width: 80px;
}

.alt-reason {
  color: #606266;
  font-size: 13px;
}
</style>
